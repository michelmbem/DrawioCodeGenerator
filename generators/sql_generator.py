from generators.code_generator import CodeGeneratorInterface


class SqlCodeGenerator(CodeGeneratorInterface):
    """
    Generate SQL code

    Parameters:
        syntax_tree: syntax_tree of the drawio file 
        file_path: path for the code files to be written to 
    """

    def __init__(self, syntax_tree, file_path):
        self.__syntax_tree = syntax_tree
        self.file_path = file_path.strip('/')
        self.__classes = []
        self.__properties = []
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

                file += self.generate_classes(_class['type'], _class['name'], None, None)
                file += self.generate_properties(_class['properties'])
                file += "\n);\n"

                self.__files.append([_class['name'], file])

            self.generate_files()

        except Exception as e:
            print(f"SqlCodeGenerator.generate_code ERROR: {e}")

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

        class_header = f"CREATE TABLE {class_name} (\n"
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
        first_prop = True

        for _, _property_def in properties.items():
            if first_prop:
                first_prop = False
            else:
                properties_string += ",\n"

            p = f"\t{_property_def['name']} {_property_def['type']}"
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

        return None

    def get_property_accessors(self):
        """
        Getter for the property accessors
        """

        return None

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

        return None

    def get_methods(self):
        """
        Getter for the methods
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
            for file in self.get_files():
                file_name = file[0] + ".sql"
                file_contents = file[1]
                with open(self.file_path + f"/{file_name}", "w") as f:
                    f.write(file_contents)
        except Exception as e:
            print(f"SqlCodeGenerator.generate_files ERROR: {e}")

    def get_files(self):
        """
        Getter for the files 
        """

        return self.__files
