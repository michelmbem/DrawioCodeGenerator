import re
import traceback

from generators.code_generator import CodeGeneratorInterface


class PhpCodeGenerator(CodeGeneratorInterface):
    """
    Generate PHP code

    Parameters:
        syntax_tree: syntax_tree of the drawio file 
        file_path: path for the code files to be written to 
    """

    def __init__(self, syntax_tree, file_path):
        self.syntax_tree = syntax_tree
        self.file_path = file_path.strip('/')
        self.files = []

    def generate_code(self):
        """
        Use the syntax tree to generate code files for the UML class diagrams 
        """

        print("<<< GENERATING CODE FILES FROM SYNTAX TREE >>>")

        CodeGeneratorInterface.ensure_dir_exists(self.file_path)

        try:
            for class_def in self.syntax_tree.values():
                file = ""

                inheritance = ""
                if len(class_def['relationships']['extends']) > 0:
                    inheritance += "extends "
                    inheritance += ",".join([self.syntax_tree[r]['name'] for r in class_def['relationships']['extends']]).strip(", ")

                implementation = ""
                if len(class_def['relationships']['implements']) > 0:
                    implementation += "implements "
                    implementation += ", ".join([self.syntax_tree[r]['name'] for r in class_def['relationships']['implements']]).strip(", ")

                interface_methods = []
                self.get_interface_methods(class_def['relationships']['implements'], interface_methods)

                file += self.generate_classes(class_def['type'], class_def['name'], inheritance, implementation)
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
            print(f"PhpCodeGenerator.generate_code ERROR: {e}")
            traceback.print_exception(e)

    def generate_classes(self, class_type, class_name, extends, implements):
        """
        Generate the class header 

        Parameters:
            class_type: type of class; 'class', 'abstract', 'interface, enum'
            class_name: name of class
            extends: the classes extended by this class
            implements: the interfaces implemented by this class

        Returns:
            class_header: class header string
        """

        class_header = f"{class_type} {class_name} {extends} {implements} {{\n"
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

        for property_def in properties.values():
            if is_enum:
                p = f"\tcase {property_def['name']};\n"
            else:
                p = f"\t{property_def['access']} ${property_def['name']};\n"

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
                getter = (f"\tpublic function get_{property_def['name']}() {{\n"
                          f"\t\treturn $this->{property_def['name']};\n\t}}\n\n")
                accessors_string += getter

                setter = (f"\tpublic function set_{property_def['name']}(${property_def['name']}) {{\n"
                          f"\t\t$this->{property_def['name']} = {property_def['name']};\n\t}}\n\n")
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
            m = f"\t{method_def['access']} function {method_def['name']}()\n\t{{\n\t}}\n\n"
            methods_string += m

            if class_type.endswith("class"):
                comment = "// ***requires implementation***"
                for interface_method in interface_methods:
                    m = (f"\t {interface_method['access']} function {interface_method['name']}()"
                         f"\n\t{{\n\t\n\t\t{comment}\n\t}}\n\n")
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
                file_name = file[0] + ".php"
                file_contents = file[1]
                with open(self.file_path + f"/{file_name}", "w") as f:
                    f.write(file_contents)
        except Exception as e:
            print(f"PhpCodeGenerator.generate_files ERROR: {e}")
            traceback.print_exception(e)
