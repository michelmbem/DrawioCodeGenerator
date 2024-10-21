import re
from generators.code_generator import CodeGeneratorInterface


class CSharpCodeGenerator(CodeGeneratorInterface):
    """
    Generate C# code

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
                    inheritance += ": "
                    inheritance += ", ".join([self.__syntax_tree[r]['name'] for r in _class['relationships']['extends']]).strip(", ")
                    
                implementation = "" 
                if len(_class['relationships']['implements']) > 0:
                    implementation += ", " if inheritance != "" else ": "
                    implementation += ", ".join([self.__syntax_tree[r]['name'] for r in _class['relationships']['implements']]).strip(", ")

                interface_methods = []
                self.get_interface_methods(_class['relationships']['implements'], interface_methods)

                file += self.generate_classes(_class['type'], _class['name'], inheritance, implementation)
                file += self.generate_properties(_class['properties'])
                if _class['type'] != "enum":
                    file += "\n"
                    if _class['type'].endswith("class"):
                        file += self.generate_property_accessors(_class['properties'])
                    file += self.generate_methods(_class['methods'], _class['properties'], _class['type'], interface_methods)
                file += "}\n"

                self.__files.append([_class['name'], file])

            self.generate_files()
        
        except Exception as e:
            print(f"CSharpCodeGenerator.generate_code ERROR: {e}")

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

        class_header = "using System;\n\n\n"
        class_header += f"public {class_type} {class_name} {extends} {implements}\n{{\n"
        class_header = re.sub(' +', ' ', class_header)
        self.__classes.append(class_header)
        return class_header
   
    def get_classes(self):
        """
        Getter for classes
        """

        return self.__classes
 
    def generate_properties(self, properties):
        """
        Generate properties for the class 

        Parameters:
            properties: dictionary of properties

        Returns:
            properties_string: string of the properties
        """

        properties_string = ""
        for _, _property_def in properties.items():
            p = f"\t{_property_def['access']} {_property_def['type']} {_property_def['name']};\n"
            self.__properties.append(p)
            properties_string += p 
 
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
                accessor_pair = (f"\tpublic {_property_def['type']} {_property_def['name'][0].upper()}"
                                 f"{_property_def['name'][1:]}\n\t{{")
                accessor_pair += f"\n\t\tget => {_property_def['name']};"
                accessor_pair += f"\n\t\tset => {_property_def['name']} = value;"
                accessors_string += f"{accessor_pair}\n\t}}\n\n"
                self.__accessors.append(accessor_pair)

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
        for _, method_value in methods.items():
            m = f"\t{method_value['access']} {method_value['return_type']} {method_value['name']}()\n\t{{\n\t}}\n\n"
            methods_string += m
            self.__methods.append(m)

            if class_type.endswith("class"):
                comment = "// ***requires implementation***"
                for interface_method in interface_methods:
                    m = (f"\t {interface_method['access']} {interface_method['return_type']} {interface_method['name']}()"
                         f"\n\t{{\n\t\n\t\t{comment}\n\t}}\n\n")
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
                file_name = file[0] + ".cs"
                file_contents = file[1]
                with open(self.file_path + f"/{file_name}", "w") as f:
                    f.write(file_contents)
        except Exception as e:
            print(f"CSharpCodeGenerator.generate_files ERROR: {e}")

    def get_files(self):
        """
        Getter for the files 
        """

        return self.__files
