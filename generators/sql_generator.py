import traceback

from os import path
from generators.code_generator import CodeGeneratorInterface


TYPE_MAPPINGS = {
    "boolean": "bit",
    "int8": "tinyint",
    "uint8": "tinyint unsigned",
    "int16": "smallint",
    "uint16": "smallint unsigned",
    "int32": "integer",
    "uint32": "integer unsigned",
    "int64": "bigint",
    "uint64": "bigint unsigned",
    "single": "float(24)",
    "double": "float(53)",
    "bigint": "decimal(36, 0)",
    "decimal": "decimal(36, 18)",
    "string": "varchar(50)",
}


def map_type(typename):
    return TYPE_MAPPINGS.get(typename.lower(), typename)


class SqlCodeGenerator(CodeGeneratorInterface):
    """
    Generate SQL code

    Parameters:
        syntax_tree: syntax_tree of the drawio file 
        file_path: path for the code files to be written to
        options: set of additional options
    """

    def __init__(self, syntax_tree, file_path, options):
        self.syntax_tree = syntax_tree
        self.file_path = path.abspath(file_path)
        self.options = options
        self.files = []

    def generate_code(self):
        """
        Use the syntax tree to generate code files for the UML class diagrams 
        """

        print("<<< GENERATING CODE FILES FROM SYNTAX TREE >>>")

        CodeGeneratorInterface.ensure_dir_exists(self.file_path)

        try:
            for class_def in self.syntax_tree.values():
                if class_def['type'] != "class":
                    continue

                file = self.generate_class_header(None, class_def['name'], None, None)
                file += self.generate_properties(class_def['properties'], None)
                file += "\n);\n"
                self.files.append((class_def['name'], file))

            self.generate_files()

        except Exception as e:
            print(f"SqlCodeGenerator.generate_code ERROR: {e}")
            traceback.print_exception(e)

    def generate_class_header(self, class_type, class_name, extends, implements):
        """
        Generate the class header 

        Parameters:
            class_type: type of class; 'class', 'abstract', 'interface'
            class_name: name of class
            extends: the classes extended by this class
            implements: the interfaces implemented by this class

        Returns:
            class_header: class header string
        """

        class_header = ""
        if self.options['package']:
            class_header += f"use {self.options['package']};\n\n"
        class_header += f"CREATE TABLE {class_name} (\n"
        return class_header

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

        for property_def in properties.values():
            if first_prop:
                first_prop = False
            else:
                properties_string += ",\n"

            p = f"\t{property_def['name']} {map_type(property_def['type'])}"
            if property_def['default_value']:
                p += f" default {property_def['default_value']}"

            properties_string += p

        return properties_string

    def generate_property_accessors(self, properties):
        """
        Generate property accessors for the class

        Parameters:
            properties: dictionary of properties

        Returns:
            accessors_string: string of the property accessors
        """

        return None

    def generate_methods(self, methods, class_type, interface_methods):
        """
        Generate methods for the class

        Parameters:
            methods: dictionary of methods
            class_type: one of class, abstract class, interface or enum
            interface_methods: methods of implemented interfaces
        
        Returns:
            methods_string: string of the methods 
        """

        return None

    def get_interface_methods(self, implements, interface_list):
        """
        Get the interface methods that require implementation
        
        Parameters:
            implements: list of interfaces
            interface_list: list of interface methods
        """

        pass

    def generate_files(self):
        """
        Write generated code to file 

        Returns:
            boolean: True if successful, False if unsuccessful
        """

        print(f"<<< WRITING FILES TO {self.file_path} >>>")

        try:
            for file in self.files:
                with open(path.join(self.file_path, f"{file[0]}.sql"), "w") as f:
                    f.write(file[1])
        except Exception as e:
            print(f"SqlCodeGenerator.generate_files ERROR: {e}")
            traceback.print_exception(e)
