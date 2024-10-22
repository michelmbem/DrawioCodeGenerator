import re
import traceback

from os import path
from generators.code_generator import CodeGeneratorInterface


TYPE_MAPPINGS = {
    "boolean": "Boolean",
    "int8": "Number",
    "uint8": "Number",
    "int16": "Number",
    "uint16": "Number",
    "int32": "Number",
    "uint32": "Number",
    "int64": "Number",
    "uint64": "Number",
    "single": "Number",
    "double": "Number",
    "bigint": "Number",
    "decimal": "Number",
    "string": "String",
    "date": "Date",
    "time": "Date",
    "datetime": "Date",
}


def map_type(typename):
    return TYPE_MAPPINGS.get(typename.lower(), typename)


def accessor_name(property_name):
    if property_name.startswith("_"):
        return property_name[1:]
    return property_name + "Prop"


def parameter_name(property_name):
    return "arg" + property_name.capitalize()


def get_parameter_list(param_types):
    _ndx = 0
    param_list = "("

    for param_type in param_types:
        if _ndx > 0:
            param_list += ", "
        param_list += f"arg{_ndx} : {param_type}"
        _ndx += 1

    param_list += ")"

    return param_list


class TsCodeGenerator(CodeGeneratorInterface):
    """
    Generate Typescript code

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
                    inheritance += "extends "
                    inheritance += ", ".join([self.syntax_tree[r]['name'] for r in class_def['relationships']['extends']]).strip(", ")
                    
                implementation = "" 
                if len(class_def['relationships']['implements']) > 0:
                    implementation += "implements "
                    implementation += ", ".join([self.syntax_tree[r]['name'] for r in class_def['relationships']['implements']]).strip(", ")

                interface_methods = []
                self.get_interface_methods(class_def['relationships']['implements'], interface_methods)

                file = self.generate_class_header(class_def['type'], class_def['name'], inheritance, implementation)
                file += self.generate_properties(class_def['properties'], class_def['type'] == "enum")
                file += "\n"
                if class_def['type'].endswith("class"):
                    file += self.generate_property_accessors(class_def['properties'])
                if class_def['type'] != "enum":
                    file += self.generate_methods(class_def['methods'], class_def['type'], interface_methods)
                file += "}\n" 

                self.files.append((class_def['name'], file))

            self.generate_files()
        
        except Exception as e:
            print(f"TypeScriptCodeGenerator.generate_code ERROR: {e}")
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

        if class_type != "enum" and len(self.options['imports']) > 0:
            for _import in self.options['imports']:
                class_header += f"import {_import};\n"
            class_header += "\n"

        class_header += f"{class_type} {class_name} {extends} {implements} {{\n"
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
        first_prop = True

        for property_def in properties.values():
            if is_enum:
                if first_prop:
                    first_prop = False
                else:
                    properties_string += ",\n"

                p = f"\t{property_def['name']}"
                if property_def['default_value']:
                    p += f" = {property_def['default_value']}"
            else:
                p = f"\t{property_def['access']} {map_type(property_def['type'])} {property_def['name']}"
                if property_def['default_value']:
                    p += f" = {property_def['default_value']}"
                p += ";\n"

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

        accessors_string = ""
        for property_def in properties.values():
            if property_def['access'] == "private":
                getter = (f"\tpublic get {accessor_name(property_def['name'])}() : {map_type(property_def['type'])}"
                          f" {{\n\t\treturn this.{property_def['name']};\n\t}}\n\n")
                accessors_string += getter

                setter = (f"\tpublic set {accessor_name(property_def['name'])}({parameter_name(property_def['name'])} :"
                          f" {map_type(property_def['type'])}) {{\n\t\tthis.{property_def['name']} ="
                          f" {parameter_name(property_def['name'])};\n\t}}\n\n")
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
            params = get_parameter_list(method_def['parameters'])
            if class_type == "interface":
                m = f"\t{method_def['name']}{params} : {map_type(method_def['return_type'])};"
            else:
                m = f"\t{method_def['access']} {method_def['name']}{params} : {map_type(method_def['return_type'])} {{\n\t}}"
            methods_string += m + "\n\n"

        if class_type.endswith("class"):
            for interface_method in interface_methods:
                params = get_parameter_list(interface_method['parameters'])
                m = f"\tpublic {interface_method['name']}{params} : {map_type(interface_method['return_type'])} {{\n\t}}"
                methods_string += m + "\n\n"

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
                with open(path.join(self.file_path, f"{file[0]}.ts"), "w") as f:
                    f.write(file[1])
        except Exception as e:
            print(f"TypeScriptCodeGenerator.generate_files ERROR: {e}")
            traceback.print_exception(e)
