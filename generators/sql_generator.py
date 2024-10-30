import traceback

from generators.code_generator import CodeGenerator
from generators.sql_dialect.sql_dialects import SQLDialects


class SqlCodeGenerator(CodeGenerator):
    """
    Generate SQL code

    Parameters:
        syntax_tree: syntax_tree of the drawio file 
        file_path: path for the code files to be written to
        options: set of additional options
    """

    def __init__(self, syntax_tree, file_path, options):
        super().__init__(syntax_tree, file_path, options)
        self.dialect = SQLDialects.get(options.get('dialect', "ansi"))

    def generate_code(self):
        """
        Use the syntax tree to generate code files for the UML class diagrams
        """

        print("<<< GENERATING CODE FILES FROM SYNTAX TREE >>>")

        try:
            self.ensure_dir_exists(self.file_path)

            for class_def in self.syntax_tree.values():
                if not (class_def['type'] in ("class", "abstract class") and len(class_def['properties']) > 0):
                    continue

                file_contents = self.generate_class_header(class_def['type'], class_def['name'], None, None, None)
                file_contents += self.generate_properties(class_def['properties'], class_def['type'] == "enum")
                file_contents += self.generate_class_footer(class_def['type'], class_def['name'])

                self.files.append((class_def['name'], file_contents))

            self.generate_files()
        except Exception as e:
            print(f"{self.__class__.__name__}.generate_code ERROR: {e}")
            traceback.print_exception(e)

    def generate_class_header(self, class_type, class_name, baseclasses, interfaces, references):
        """
        Generate the class header

        Parameters:
            class_type: type of class; 'class', 'abstract class', 'interface' or 'enum'
            class_name: name of class
            baseclasses: the classes extended by this class
            interfaces: the interfaces implemented by this class
            references: other classes referenced by this class

        Returns:
            class_header: class header string
        """

        class_header = ""
        if self.options['package']:
            class_header += self.package_directive(self.options['package'])
        class_header += f"CREATE TABLE {class_name} (\n"
        return class_header

    def generate_class_footer(self, class_type, class_name):
        """
        Generate the class footer

        Parameters:
            class_type: type of class; 'class', 'abstract class', 'interface' or 'enum'
            class_name: name of class

        Returns:
            properties_string: the closing brace of a class definition
        """

        return "\n);\n"

    def generate_properties(self, properties, _):
        """
        Generate properties for the class

        Parameters:
            properties: dictionary of properties
            _: ignored! should tell if we are generating enum members

        Returns:
            properties_string: string of the properties
        """

        properties_string = ""
        first_prop = True
        primary_key = []
        foreign_keys = {}

        for property_def in properties.values():
            constraints = property_def['constraints']

            if first_prop:
                first_prop = False
            else:
                properties_string += ",\n"

            p = f"\t{property_def['name']} {self.map_type(property_def['type'], constraints)}"

            if constraints.get('required', False):
                p += " not null"
            if constraints.get('unique', False):
                p += " unique"
            if constraints.get('identity', False):
                p += f" {self.dialect.identity_spec()}".rstrip()
            if constraints.get('pk', False):
                primary_key += [property_def['name']]
            if constraints.get('fk', False):
                fk_target = constraints['fk_target']
                if fk_target in foreign_keys:
                    foreign_keys[fk_target].append(property_def['name'])
                else:
                    foreign_keys[fk_target] = [property_def['name']]

            if property_def['default_value']:
                p += f" default {property_def['default_value']}"

            properties_string += p

        if len(primary_key) > 0:
            properties_string += f",\n\tprimary key({', '.join(primary_key)})"

        for foreign_table, columns in foreign_keys.items():
            properties_string += f",\n\tforeign key({', '.join(columns)}) references {foreign_table}"

        return properties_string

    def generate_property_accessors(self, class_name, properties):
        return None

    def generate_methods(self, methods, class_type, interface_methods):
        return None

    def generate_default_ctor(self, class_name):
        return ""

    def generate_full_arg_ctor(self, class_name, properties):
        return ""

    def generate_equal_hashcode(self, class_name, properties):
        return ""

    def generate_to_string(self, class_name, properties):
        return ""

    def package_directive(self, package_name):
        return f"use {'_'.join(self.split_package_name(package_name))};\n\n"

    def map_type(self, typename, constraints = None):
        return self.dialect.map_type(typename, constraints)

    def default_value(self, typename):
        typename = typename.lower()
        if typename == "boolean":
            return "False"
        if typename in ("int8", "uint8", "int16", "uint16", "int32", "uint32",
                        "int64", "uint64", "single", "double", "bigint", "decimal"):
            return "0"
        if typename == "string":
            return '""'
        return "None"

    def get_parameter_list(self, param_types):
        return ""

    def get_file_extension(self):
        return "sql"
