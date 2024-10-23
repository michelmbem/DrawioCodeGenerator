from generators.code_generator import CodeGenerator


class PhpCodeGenerator(CodeGenerator):
    """
    Generate PHP code

    Parameters:
        syntax_tree: syntax_tree of the drawio file 
        file_path: path for the code files to be written to
        options: set of additional options
    """

    def __init__(self, syntax_tree, file_path, options):
        CodeGenerator.__init__(self, syntax_tree, file_path, options)

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

        class_header = "<?php\n"

        if self.options['package']:
            class_header += f"namespace {self.options['package']};\n\n"

        if class_type != "enum":
            add_linebreak = False

            for module, symbols in self.options['imports'].items():
                class_header += f"require_once '{module}';\n"
                add_linebreak = True

            for baseclass in baseclasses:
                class_header += f"require_once './{baseclass}.php';\n"
                add_linebreak = True

            for interface in interfaces:
                class_header += f"require_once './{interface}.php';\n"
                add_linebreak = True

            for reference in references:
                class_header += f"require_once './{reference}.php';\n"
                add_linebreak = True

            if add_linebreak:
                class_header += "\n"

        class_header += f"{class_type} {class_name}"
        if len(baseclasses) > 0:
            class_header += f" extends {baseclasses[0]}"
        if len(interfaces) > 0:
            class_header += f" implements {', '.join(interfaces)}"
        class_header += " {\n"

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

        return "}\n"

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
                p = f"\tcase {property_def['name']}"
            else:
                p = f"\t{property_def['access']} ${property_def['name']}"

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
                getter = (f"\tpublic function get_{property_def['name']}() {{\n"
                          f"\t\treturn $this->{property_def['name']};\n\t}}\n\n")
                accessors_string += getter

                setter = (f"\tpublic function set_{property_def['name']}(${property_def['name']}) {{\n"
                          f"\t\t$this->{property_def['name']} = ${property_def['name']};\n\t}}\n\n")
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
            params = self.get_parameter_list(method_def['parameters'])
            if class_type == "interface":
                m = f"\t{method_def['access']} function {method_def['name']}{params};"
            else:
                m = f"\t{method_def['access']} function {method_def['name']}{params}\n\t{{\n\t}}"
            methods_string += m + "\n\n"

        if class_type.endswith("class"):
            for interface_method in interface_methods:
                params = self.get_parameter_list(interface_method['parameters'])
                m = f"\t{interface_method['access']} function {interface_method['name']}{params}\n\t{{\n\t}}"
                methods_string += m + "\n\n"

        return methods_string

    def map_type(self, typename):
        return None

    def default_value(self, typename):
        return None

    def get_parameter_list(self, param_types):
        param_list = "("

        for _ndx in range(len(param_types)):
            if _ndx > 0:
                param_list += ", "
            param_list += f"$arg{_ndx}"

        param_list += ")"

        return param_list

    def get_file_extension(self):
        return "php"
