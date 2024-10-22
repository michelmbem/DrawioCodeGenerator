import re
import traceback

from os import path
from generators.code_generator import CodeGeneratorInterface


def accessor_name(property_name):
    if property_name.startswith("_"):
        return property_name[1:]
    return property_name + "Prop"


def parameter_name(property_name):
    return "arg" + property_name.capitalize()


def default(typename):
    typename = typename.lower()
    if typename == "boolean":
        return "False"
    if typename in ("int8", "uint8", "int16", "uint16", "int32", "uint32",
                    "int64", "uint64", "single", "double", "bigint", "decimal"):
        return "0"
    if typename == "string":
        return '""'
    return "None"


def get_parameter_list(param_types):
    param_list = "("

    for _ndx in range(len(param_types)):
        if _ndx > 0:
            param_list += ", "
        param_list += f"arg{_ndx}"

    param_list += ")"

    return param_list


class PythonCodeGenerator(CodeGeneratorInterface):
    """
    Generate Python code

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
                inheritance = ""
                if len(class_def['relationships']['extends']) > 0:
                    inheritance = ", ".join([self.syntax_tree[r]['name'] for r in class_def['relationships']['extends']]).strip(", ")

                implementation = ""
                if len(class_def['relationships']['implements']) > 0:
                    implementation = ", ".join([self.syntax_tree[r]['name'] for r in class_def['relationships']['implements']]).strip(", ")

                interface_methods = []
                self.get_interface_methods(class_def['relationships']['implements'], interface_methods)

                file = self.generate_class_header(class_def['type'], class_def['name'], inheritance, implementation)
                if len(class_def['properties']) <= 0 and len(class_def['methods']) <= 0 and len(interface_methods) <= 0:
                    file += "\tpass\n"
                else:
                    file += self.generate_properties(class_def['properties'], class_def['type'] == "enum")
                    file += "\n"
                    if class_def['type'].endswith("class"):
                        file += self.generate_property_accessors(class_def['properties'])
                    if class_def['type'] != "enum":
                        file += self.generate_methods(class_def['methods'], class_def['type'], interface_methods)

                self.files.append((class_def['name'], file))

            self.generate_files()

        except Exception as e:
            print(f"PythonCodeGenerator.generate_code ERROR: {e}")
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

        if class_type == "enum":
            class_header += "from enum import Enum, auto\n"
            class_ancestors = "(Enum)"
        else:
            for _import in self.options['imports']:
                class_header += f"import {_import}\n"

            class_header += "from abc import ABC, abstractmethod\n"

            class_ancestors = "(ABC"
            if extends:
                class_ancestors += f", {extends}"
            if implements:
                class_ancestors += f", {implements}"
            class_ancestors += ")"

        class_header += "\n\n"
        class_header += f"class {class_name}{class_ancestors}:\n"
        class_header = re.sub(' +', ' ', class_header)

        return class_header

    def generate_properties(self, properties, is_enum):
        """
        Generate properties for the class

        Parameters:
            properties: dictionary of properties
            is_enum: tells if we are generating enum members

        Returns:
            properties_string: string of the properties
        """

        properties_string = ""
        met_property = False

        if not is_enum:
            properties_string = "\tdef __init__(self):\n"

        for property_def in properties.values():
            if is_enum:
                p = f"\t{property_def['name']}"
                if property_def['default_value']:
                    p += f" = {property_def['default_value']}"
                else:
                    p += " = auto()"
            else:
                p = f"\t\tself.{property_def['name']}"
                if property_def['default_value']:
                    p += f" = {property_def['default_value']}"
                else:
                    p += f" = {default(property_def['type'])}"

            p += "\n"

            properties_string += p
            met_property = True

        if not met_property:
            properties_string += "\t\tpass\n"

        return properties_string

    def generate_property_accessors(self, properties):
        """
        Generate property accessors for the class

        Parameters:
            properties: dictionary of properties

        Returns:
            accessors_string: string of the property accessors
        """

        accessors_string = ""
        for property_def in properties.values():
            if property_def['access'] == "private":
                getter = (f"\t@property\n\tdef {accessor_name(property_def['name'])}(self):\n"
                          f"\t\treturn self.{property_def['name']}\n\n")
                accessors_string += getter

                setter = (f"\t@{accessor_name(property_def['name'])}.setter\n\tdef {accessor_name(property_def['name'])}"
                          f"(self, {parameter_name(property_def['name'])}):\n\t\tself.{property_def['name']} ="
                          f" {parameter_name(property_def['name'])}\n\n")
                accessors_string += setter

        return accessors_string

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

        methods_string = ""

        for method_def in methods.values():
            m = ""
            if class_type in ("interface", "abstract class"):
                m += "\t@abstractmethod\n"
            m += f"\tdef {method_def['name']}(self):\n\t\tpass\n\n"
            methods_string += m

        # inherited abstract methods
        if class_type.endswith("class"):
            comment = "# ***requires implementation***"
            for interface_method in interface_methods:
                m = f"\tdef {interface_method['name']}(self):\n\t\t{comment}\n\t\tpass\n\n"
                methods_string += m

        return methods_string

    def get_interface_methods(self, implements, interface_list):
        """
        Get the interface methods that require implementation
        
        Parameters:
            implements: list of interfaces
            interface_list: list of interface methods
        """

        for i in implements:
            interface_obj = self.syntax_tree[i]
            interface_list += interface_obj['methods'].values()
            self.get_interface_methods(interface_obj['relationships']['implements'], interface_list)

    def generate_files(self):
        """
        Write generated code to file 

        Returns:
            boolean: True if successful, False if unsuccessful
        """

        print(f"<<< WRITING FILES TO {self.file_path} >>>")

        try:
            for file in self.files:
                with open(path.join(self.file_path, f"{file[0]}.py"), "w") as f:
                    f.write(file[1])
        except Exception as e:
            print(f"PythonCodeGenerator.generate_files ERROR: {e}")
            traceback.print_exception(e)
