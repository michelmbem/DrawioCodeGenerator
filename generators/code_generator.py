import re
import traceback

from os import makedirs, path
from abc import ABC, abstractmethod


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

    @staticmethod
    def ensure_dir_exists(dir_path):
        makedirs(dir_path, exist_ok=True)

    @staticmethod
    def split_package_name(package_name):
        return re.split(r"[./\\:]+", package_name)

    def generate_code(self):
        """
        Use the syntax tree to generate code files for the UML class diagrams
        """

        print("<<< GENERATING CODE FILES FROM SYNTAX TREE >>>")

        try:
            self.ensure_dir_exists(self.file_path)

            for class_def in self.syntax_tree.values():
                baseclasses, interfaces, references = self.get_class_dependencies(class_def)

                file_contents = self.generate_class_header(class_def['type'], class_def['name'], baseclasses, interfaces, references)
                file_contents += self.generate_properties(class_def['properties'], class_def['type'] == "enumeration")
                file_contents += "\n"

                if class_def['type'] in ("class", "abstract class"):
                    class_has_props = len(class_def['properties']) > 0
                    should_generate = self.options['generate']

                    if should_generate['default_ctor']:
                        file_contents += self.generate_default_ctor(class_def['name'])

                    if class_has_props and should_generate['full_arg_ctor']:
                        file_contents += self.generate_full_arg_ctor(class_def['name'], class_def['properties'])

                    file_contents += self.generate_property_accessors(class_def['properties'])

                    if class_has_props and should_generate['equal_hashcode']:
                        file_contents += self.generate_equal_hashcode(class_def['name'], class_def['properties'])

                    if class_has_props and should_generate['to_string']:
                        file_contents += self.generate_to_string(class_def['name'], class_def['properties'])

                if class_def['type'] != "enumeration":
                    interface_methods = []
                    self.get_interface_methods(class_def['relationships']['implements'], interface_methods)
                    file_contents += self.generate_methods(class_def['methods'], class_def['type'], interface_methods)

                file_contents += self.generate_class_footer(class_def['type'], class_def['name'])

                self.files.append((class_def['name'], file_contents))

            self.generate_files()
        except Exception as e:
            print(f"{self.__class__.__name__}.generate_code ERROR: {e}")
            traceback.print_exception(e)

    def generate_files(self):
        """
        Write generated code to file

        Returns:
            boolean: True if successful, False if unsuccessful
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

        baseclasses = []
        if len(class_def['relationships']['extends']) > 0:
            baseclasses += [self.syntax_tree[r]['name'] for r in class_def['relationships']['extends']]

        interfaces = []
        if len(class_def['relationships']['implements']) > 0:
            interfaces += [self.syntax_tree[r]['name'] for r in class_def['relationships']['implements']]

        references = []
        if len(class_def['relationships']['association']) > 0:
            references += [self.syntax_tree[r]['name'] for r in class_def['relationships']['association']]
        if len(class_def['relationships']['aggregation']) > 0:
            references += [self.syntax_tree[r]['name'] for r in class_def['relationships']['aggregation']]
        if len(class_def['relationships']['composition']) > 0:
            references += [self.syntax_tree[r]['name'] for r in class_def['relationships']['composition']]

        class_methods = [*class_def['methods'].values()]
        if class_def['type'] in ("class", "abstract class"):
            self.get_interface_methods(class_def['relationships']['implements'], class_methods)

        for other_class in self.syntax_tree.values():
            for property_def in class_def['properties'].values():
                if property_def['type'] == other_class['name']:
                    references += [other_class['name']]

            for method_def in class_methods:
                if method_def['return_type'] == other_class['name']:
                    references += [other_class['name']]

                for parameter in method_def['parameters']:
                    if parameter['type'] == other_class['name']:
                        references += [other_class['name']]

        return baseclasses, interfaces, references

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

    def get_property_access(self, property_def):
        return "private" if self.options['encapsulate_all_props'] else property_def['access']

    @abstractmethod
    def generate_class_header(self, class_type, class_name, baseclasses, interfaces, references):
        pass

    @abstractmethod
    def generate_class_footer(self, class_type, class_name):
        pass
    
    @abstractmethod
    def generate_properties(self, properties, is_enum):
        pass

    @abstractmethod
    def generate_property_accessors(self, properties):
        pass

    @abstractmethod
    def generate_methods(self, methods, class_type, interface_methods):
        pass

    @abstractmethod
    def generate_default_ctor(self, class_name):
        pass

    @abstractmethod
    def generate_full_arg_ctor(self, class_name, properties):
        pass

    @abstractmethod
    def generate_equal_hashcode(self, class_name, properties):
        pass

    @abstractmethod
    def generate_to_string(self, class_name, properties):
        pass

    @abstractmethod
    def package_directive(self, package_name):
        pass

    @abstractmethod
    def map_type(self, typename):
        pass

    @abstractmethod
    def default_value(self, typename):
        pass

    @abstractmethod
    def get_parameter_list(self, param_types):
        pass

    @abstractmethod
    def get_file_extension(self):
        pass
