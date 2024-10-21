import re
from generators.code_generator import CodeGeneratorInterface


def accessor_name(property_name):
    if property_name.startswith("_"):
        return property_name[1:]
    return property_name + "Prop"


def parameter_name(property_name):
    return "arg" + property_name.capitalize()


class PythonCodeGenerator(CodeGeneratorInterface):
    """
    Generate Python code

    Parameters:
        syntax_tree: syntax_tree of the drawio file 
        file_path: path for the code files to be written to 
    """

    def __init__(self, syntax_tree, file_path):
        self.__syntax_tree = syntax_tree
        self.file_path = file_path.strip('/')
        self.__classes = []
        self.__properties = []
        self.__accessors = []
        self.__methods = []
        self.__files = []

    def generate_code(self):
        """
        Use the syntax tree to generate code files for the UML class diagrams 
        """

        print("<<< GENERATING CODE FILES FROM SYNTAX TREE >>>")

        CodeGeneratorInterface.ensure_dir_exists(self.file_path)

        try:
            for _, _class in self.__syntax_tree.items():
                file = ""

                inheritance = ""
                if len(_class['relationships']['extends']) > 0:
                    inheritance = ", ".join([self.__syntax_tree[r]['name'] for r in _class['relationships']['extends']]).strip(", ")

                implementation = ""
                if len(_class['relationships']['implements']) > 0:
                    implementation = ", ".join([self.__syntax_tree[r]['name'] for r in _class['relationships']['implements']]).strip(", ")

                interface_methods = []
                self.get_interface_methods(_class['relationships']['implements'], interface_methods)

                file += self.generate_classes(_class['type'], _class['name'], inheritance, implementation)
                if _class['type'] == "enum":
                    file += self.generate_properties(_class['properties'], True)
                else:
                    file += self.generate_properties(_class['properties'], False)
                    file += "\n"
                    if _class['type'].endswith("class"):
                        file += self.generate_property_accessors(_class['properties'])
                    file += self.generate_methods(_class['methods'], _class['properties'], _class['type'], interface_methods)

                self.__files.append([_class['name'], file])

            self.generate_files()

        except Exception as e:
            print(f"PythonCodeGenerator.generate_code ERROR: {e}")

    def generate_classes(self, class_type, class_name, extends, implements):
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

        if class_type == "enum":
            class_header = "from enum import Enum, auto\n\n\n"
            class_ancestors = "(Enum)"
        else:
            class_header = "from abc import ABC, abstractmethod\n\n\n"
            class_ancestors = "(" + f"ABC, {extends}, {implements}".strip(", ") + ")"

        class_header += f"class {class_name}{class_ancestors}:\n"
        class_header = re.sub(' +', ' ', class_header)
        self.__classes.append(class_header)
        return class_header

    def get_classes(self):
        """
        Getter for classes
        """

        return self.__classes

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

        for _, _property_def in properties.items():
            if is_enum:
                p = f"\t{_property_def['name']} = auto()\n"
            else:
                p = f"\t\tself.{_property_def['name']} = None\n"

            properties_string += p
            self.__properties.append(p)

        return properties_string

    def get_properties(self):
        """
        Getter for properties
        """

        return self.__properties

    def generate_property_accessors(self, properties):
        """
        Generate property accessors for the class

        Parameters:
            properties: dictionary of properties

        Returns:
            accessors_string: string of the property accessors
        """

        accessors_string = ""
        for _, _property_def in properties.items():
            if _property_def['access'] == "private":
                getter = (f"\t@property\n\tdef {accessor_name(_property_def['name'])}(self):\n"
                          f"\t\treturn self.{_property_def['name']}\n\n")
                accessors_string += getter
                self.__accessors.append(getter)

                setter = (f"\t@{accessor_name(_property_def['name'])}.setter\n\tdef {accessor_name(_property_def['name'])}"
                          f"(self, {parameter_name(_property_def['name'])}):\n\t\tself.{_property_def['name']} ="
                          f" {parameter_name(_property_def['name'])}\n\n")
                accessors_string += setter
                self.__accessors.append(setter)

        return accessors_string

    def get_property_accessors(self):
        """
        Getter for the property accessors
        """

        return self.__accessors

    def generate_methods(self, methods, properties, class_type, interface_methods):
        """
        Generate methods for the class

        Parameters:
            methods: dictionary of methods
            properties: dictionary of properties
            class_type: type of current class
            interface_methods: methods of implemented interfaces
        
        Returns:
            methods_string: string of the methods 
        """

        methods_string = ""
        for _, method_def in methods.items():
            m = f"\tdef {method_def['name']}(self):\n\t\tpass\n\n"
            methods_string += m
            self.__methods.append(m)

        # inherited abstract methods
        if class_type.endswith("class"):
            comment = "# ***requires implementation***"
            for interface_method in interface_methods:
                m = f"\tdef {interface_method['name']}(self):\n\t\t{comment}\n\t\tpass\n\n"
                methods_string += m
                self.__methods.append(m)

        return methods_string

    def get_methods(self):
        """
        Getter for the methods
        """

        return self.__methods

    def get_interface_methods(self, implements, interface_list):
        """
        Get the interface methods that require implementation
        
        Parameters:
            implements: list of interfaces
            interface_list: list of interface methods
        """

        for i in implements:
            interface_obj = self.__syntax_tree[i]
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
            for file in self.get_files():
                file_name = file[0] + ".py"
                file_contents = file[1]
                with open(self.file_path + f"/{file_name}", "w") as f:
                    f.write(file_contents)
        except Exception as e:
            print(f"PythonCodeGenerator.generate_files ERROR: {e}")

    def get_files(self):
        """
        Getter for the files 
        """

        return self.__files
