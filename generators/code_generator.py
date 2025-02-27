import re
import traceback

from operator import itemgetter
from copy import deepcopy
from os import makedirs, path
from abc import ABC, abstractmethod


INTEGRAL_TYPE = re.compile(r"^(?:u(?:nsigned\s+)?)?(?:short|int(?:16|32|64|eger)?|long)$", re.IGNORECASE)


class CodeGenerator(ABC):
    """
    Base class of all code generators

    Parameters:
        syntax_tree: syntax tree of the drawio file
        file_path: path for the code files to be written to
        options: set of additional options
    """

    def __init__(self, syntax_tree, file_path, options):
        self.syntax_tree = syntax_tree
        self.file_path = path.abspath(file_path)
        self.options = options
        self.files = []

        self.defined_types = { class_def['name']: class_id for class_id, class_def in syntax_tree.items() }

        if options['infer_keys']:
            self.infer_keys_from_names(options['pk_pattern'])

    @staticmethod
    def ensure_dir_exists(dir_path):
        makedirs(dir_path, exist_ok=True)

    @staticmethod
    def split_package_name(package_name):
        return re.split(r"[./\\:]+", package_name)

    def infer_keys_from_names(self, pk_pattern):
        syntax_tree = deepcopy(self.syntax_tree)

        for class_def in syntax_tree.values():
            matcher = re.compile(pk_pattern.replace("@class", class_def['name']), re.IGNORECASE)
            pk_found, pk_candidate = False, None

            for property_def in class_def['properties'].values():
                if property_def['constraints'].get("pk"):
                    pk_found = True
                    break

                if matcher.match(property_def['name']):
                    pk_candidate = property_def

            if pk_candidate and not pk_found:
                pk_candidate['constraints']['pk'] = True
                is_integer = INTEGRAL_TYPE.match(pk_candidate['type'])
                pk_candidate['constraints']['identity'] = is_integer

        self.syntax_tree = syntax_tree

    def generate_code(self):
        """
        Use the syntax tree to generate code files for the UML class diagrams
        """

        print("<<< GENERATING CODE FILES FROM SYNTAX TREE >>>")

        try:
            self.ensure_dir_exists(self.file_path)

            for class_def in self.syntax_tree.values():
                get_items = itemgetter("name", "type", "properties")
                class_name, class_type, properties = get_items(class_def)
                baseclasses, interfaces, references = self.get_class_dependencies(class_def)

                file_contents = self.generate_class_header(class_type, class_name, baseclasses, interfaces, references)
                file_contents += self.generate_properties(class_type, class_name, properties, references)
                file_contents += "\n"

                if class_type in ("class", "abstract class"):
                    inherited_props = []
                    self.get_inherited_instance_props(class_def, inherited_props)
                    declared_props = {k: p for k, p in properties.items() if not p['constraints'].get("static")}
                    has_instance_props = len(declared_props) + len(inherited_props) > 0
                    should_generate = self.options['generate']

                    if should_generate['default_ctor']:
                        file_contents += self.generate_default_ctor(class_name, baseclasses)

                    if has_instance_props and should_generate['full_arg_ctor']:
                        file_contents += self.generate_full_arg_ctor(class_name, baseclasses, declared_props, inherited_props)

                    file_contents += self.generate_property_accessors(class_name, properties, references)

                    if has_instance_props and should_generate['equal_hashcode']:
                        file_contents += self.generate_equal_hashcode(class_name, baseclasses, declared_props)

                    if has_instance_props and should_generate['to_string']:
                        file_contents += self.generate_to_string(class_name, baseclasses, declared_props)

                if class_type != "enum":
                    interface_methods = []
                    self.get_interface_methods(class_def['relationships']['implements'], interface_methods)
                    file_contents += self.generate_methods(class_type, class_def['methods'], interface_methods)

                file_contents += self.generate_class_footer(class_type, class_name)

                self.files.append((class_name, file_contents))

            self.generate_files()
        except Exception as e:
            print(f"{self.__class__.__name__}.generate_code ERROR: {e}")
            traceback.print_exception(e)

    def generate_files(self):
        """
        Write generated code to file
        """

        print(f"<<< WRITING FILES TO {self.file_path} >>>")

        try:
            for filename, contents in self.files:
                file_path = path.join(self.file_path, f"{filename}.{self.get_file_extension()}")
                with open(file_path, "w") as f:
                    f.write(contents)
        except Exception as e:
            print(f"{self.__class__.__name__}.generate_files ERROR: {e}")
            traceback.print_exception(e)

    def get_class_dependencies(self, class_def):
        """
        Get a tuple of all the classes that this class depends on

        :param class_def: the current class
        :return: a tuple of baseclasses, implemented interfaces and referenced classes
        """

        get_items = itemgetter('extends', 'implements', 'association', 'aggregation', 'composition')
        extends, implements, association, aggregation, composition = get_items(class_def['relationships'])

        baseclasses = [self.syntax_tree[r]['name'] for r in extends]
        interfaces = [self.syntax_tree[r]['name'] for r in implements]
        references = [(r[0], self.syntax_tree[r[1]]['name'], False) for r in association]
        references += [(r[0], self.syntax_tree[r[1]]['name'], False) for r in aggregation]
        references += [(r[0], self.syntax_tree[r[1]]['name'], True) for r in composition]

        class_methods = [*class_def['methods'].values()]
        if class_def['type'] in ("class", "abstract class"):
            self.get_interface_methods(implements, class_methods)

        for other_class in self.syntax_tree.values():
            other_class_name = other_class['name']

            for property_def in class_def['properties'].values():
                if property_def['type'] == other_class_name:
                    references.append(('uses', other_class_name, False))

            for method_def in class_methods:
                if method_def['return_type'] == other_class_name:
                    references.append(('uses', other_class_name, False))

                for parameter in method_def['parameters']:
                    if parameter['type'] == other_class_name:
                        references.append(('uses', other_class_name, False))

        return baseclasses, interfaces, references

    def get_inherited_instance_props(self, class_def, properties):
        """
        Get a collection of all non-static properties of the ancestors of the given class

        Parameters:
            class_def: the given class
            properties: list of inherited instance properties
        """

        parents = [self.syntax_tree[r] for r in class_def['relationships']['extends']]

        for parent in parents:
            self.get_inherited_instance_props(parent, properties)
            properties += [p for p in parent['properties'].values() if not p['constraints'].get("static")]

    def get_interface_methods(self, interface_ids, interface_methods):
        """
        Get the interface methods that require implementation

        Parameters:
            interface_ids: list of interface ids
            interface_methods: list of interface methods
        """

        for interface_id in interface_ids:
            interface = self.syntax_tree[interface_id]
            interface_methods += interface['methods'].values()
            self.get_interface_methods(interface['relationships']['implements'], interface_methods)

    def get_class_by_name(self, class_name):
        class_id = self.defined_types.get(class_name)
        return self.syntax_tree.get(class_id) if class_id else None

    def get_stereotype(self, class_name):
        class_def = self.get_class_by_name(class_name)
        return class_def['stereotype'] if class_def else None

    def get_primary_key(self, class_name):
        """
        Searches for the set of properties that represent the primary key of an entity

        Parameters:
            class_name: the class name
        """

        class_def = self.get_class_by_name(class_name)
        if class_def:
            pk = [p for p in class_def['properties'].values() if p['constraints'].get("pk")]
            if len(pk) > 0: return pk

            baseclasses = [self.syntax_tree[r]['name'] for r in class_def['relationships']['extends']]
            for baseclass in baseclasses:
                pk = self.get_primary_key(baseclass)
                if len(pk) > 0: return pk

        return []

    def get_property_access(self, property_def):
        return "private" if self.options['encapsulate_all_props'] else property_def['access']

    def generate_property_accessors(self, class_name, properties, references):
        return ""

    def generate_methods(self, class_type, methods, interface_methods):
        return ""

    def generate_default_ctor(self, class_name, baseclasses):
        return ""

    def generate_full_arg_ctor(self, class_name, baseclasses, properties, inherited_properties):
        return ""

    def generate_equal_hashcode(self, class_name, baseclasses, properties):
        return ""

    def generate_to_string(self, class_name, baseclasses, properties):
        return ""

    def package_directive(self, package_name):
        return ""

    def map_type(self, typename, constraints = None):
        return self.TYPE_MAPPINGS.get(typename.lower(), typename)

    def default_value(self, typename):
        typename = typename.lower()
        if typename in ("boolean", "bool"):
            return "false"
        if typename in ("sbyte", "int8", "byte", "uint8", "short", "int16", "ushort", "uint16",
                        "integer", "int", "int32", "uint", "uint32", "long", "int64", "ulong",
                        "uint64", "float", "single", "double", "bigint", "decimal"):
            return "0"
        if typename in ("char", "wchar", "string", "wstring"):
            return '""'
        return None

    def get_parameter_list(self, param_types):
        return ""

    @abstractmethod
    def generate_class_header(self, class_type, class_name, baseclasses, interfaces, references):
        pass

    @abstractmethod
    def generate_class_footer(self, class_type, class_name):
        pass

    @abstractmethod
    def generate_properties(self, class_type, class_name, properties, references):
        pass

    @abstractmethod
    def get_file_extension(self):
        pass
