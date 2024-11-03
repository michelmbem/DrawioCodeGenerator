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
        super().__init__(syntax_tree, file_path, options)

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
            class_header += self.package_directive(self.options['package'])

        if class_type != "enum":
            imports = set()

            for module, symbols in self.options['imports'].items():
                imports.add(f"require_once '{module}';")

            dependencies = {*baseclasses, *interfaces, *references}
            imports |= set(f"require_once './{dependency}.php';" for dependency in dependencies if dependency != class_name)

            for import_line in sorted(imports):
                class_header += f"{import_line}\n"

            if len(imports) > 0:
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
                modifier = f"{self.get_property_access(property_def)}"
                constraints = property_def['constraints']
                dollar = '$'

                if constraints.get('static', False):
                    if constraints.get('final', False):
                        modifier = f"{property_def['access']} const"
                        dollar = ''
                    else:
                        modifier += " static"
                elif constraints.get('final', False):
                    modifier += " final"

                p = f"\t{modifier} {dollar}{property_def['name']}"

            if property_def['default_value']:
                p += f" = {property_def['default_value']}"

            p += ";\n"
            properties_string += p

        return properties_string

    def generate_property_accessors(self, class_name, properties):
        """
        Generate property accessors for the class

        Parameters:
            class_name: name of class
            properties: dictionary of properties

        Returns:
            accessors_string: string of the property accessors
        """

        accessors_string = ""

        for property_def in properties.values():
            if self.get_property_access(property_def) == "private":
                constraints = property_def['constraints']
                modifier, target = " ", "$this->"

                if constraints.get('static', False):
                    if constraints.get('final', False):
                        continue    # No encapsulation for constants
                    modifier = " static "
                    target = f"{class_name}::"

                getter = (f"\tpublic{modifier}function get_{property_def['name']}() {{\n"
                          f"\t\treturn {target}{property_def['name']};\n\t}}\n\n")
                accessors_string += getter

                if not constraints.get('final', False):
                    setter = (f"\tpublic{modifier}function set_{property_def['name']}(${property_def['name']}) {{\n"
                              f"\t\t{target}{property_def['name']} = ${property_def['name']};\n\t}}\n\n")
                    accessors_string += setter

        return accessors_string

    def generate_methods(self, methods, class_type, interface_methods):
        """
        Generate methods for the class

        Parameters:
            methods: dictionary of methods
            class_type: type of class; 'class', 'abstract class' or 'interface'
            interface_methods: methods of implemented interfaces
        
        Returns:
            methods_string: string of the methods 
        """

        methods_string = ""
        comment = "// Todo: implement this method!"

        for method_def in methods.values():
            params = self.get_parameter_list(method_def['parameters'])

            if class_type == "interface":
                m = f"\t{method_def['access']} function {method_def['name']}{params};"
            else:
                constraints = method_def['constraints']

                modifier = ""
                if constraints.get('static', False):
                    modifier += " static"
                elif constraints.get('abstract', False):
                    modifier += " abstract"
                elif constraints.get('final', False):
                    modifier += " final"
                modifier += " "

                m = f"\t{method_def['access']}{modifier}function {method_def['name']}{params}"
                if constraints.get('abstract', False):
                    m += ";\n"
                else:
                    m += f" \t{{\n\t\t{comment}\n"
                    if method_def['return_type'] != "void":
                        m += f"\t\treturn {self.default_value(method_def['return_type'])};\n"
                    m += "\t}"

            methods_string += m + "\n\n"

        if class_type in ("class", "abstract class"):
            for interface_method in interface_methods:
                params = self.get_parameter_list(interface_method['parameters'])
                m = f"\t{interface_method['access']} function {interface_method['name']}{params} \t{{\n"
                m += f"\t\t{comment}\n"
                if interface_method['return_type'] != "void":
                    m += f"\t\treturn {self.default_value(interface_method['return_type'])};\n"
                m += "\t}"
                methods_string += m + "\n\n"

        return methods_string

    def generate_full_arg_ctor(self, class_name, properties, call_super, inherited_properties):
        separator = ",\n\t\t\t" if len(properties) > 4 else ", "
        ctor_string = "\tpublic function __construct("
        if call_super:
            ctor_string += separator.join(f"${p['name']} = {self.default_value(p['type'])}" for p in inherited_properties)
            if not ctor_string.endswith('(') and len(properties) > 0:
                ctor_string += ", "
        ctor_string += separator.join(f"${p['name']} = {self.default_value(p['type'])}" for p in properties.values())
        ctor_string += ") {\n"
        if call_super:
            ctor_string += f"\t\tparent::__construct({', '.join(f"${p['name']}" for p in inherited_properties)});\n"
        ctor_string += '\n'.join(f"\t\t$this->{p['name']} = ${p['name']};" for p in properties.values())
        ctor_string += "\n\t}\n\n"

        return ctor_string

    def generate_equal_hashcode(self, class_name, properties, call_super):
        method_string = "\tpublic function equals($obj) {\n"
        method_string += "\t\tif ($this === $obj) return true;\n"
        method_string += "\t\tif (get_class($this) === get_class($obj)) {\n\t\t\treturn "
        if call_super:
            method_string += "parent::equals($obj)"
            if len(properties) > 0:
                method_string += " &&\n\t\t\t\t"
        method_string += " &&\n\t\t\t\t".join(f"$this->{p['name']} === $obj->{p['name']}" for p in properties.values())
        method_string += ";\n\t\t}\n\t\treturn false;\n\t}\n\n"

        method_string += "\tpublic function hashCode() {\n"
        method_string += "\t\treturn crc32(\""
        method_string += ':'.join(f"$this->{p['name']}" for p in properties.values())
        method_string += "\");\n\t}\n\n"

        return method_string

    def generate_to_string(self, class_name, properties, call_super):
        method_string = "\tpublic function toString() {\n"
        if call_super:
            method_string += "\t\t$parentString = parent::toString();\n"
        method_string += f"\t\treturn \"{class_name} \\{{"
        if call_super:
            method_string += "$parentString"
            if len(properties) > 0:
                method_string += ", "
        method_string += ', '.join(f"{p['name']}=$this->{p['name']}" for p in properties.values())
        method_string += "\\}\";\n\t}\n\n"

        return method_string

    def package_directive(self, package_name):
        return f"namespace {'\\'.join(self.split_package_name(package_name))};\n\n"

    def default_value(self, typename):
        return super().default_value(typename) or "null"

    def get_parameter_list(self, parameters):
        return f"({', '.join(f"${p['name']}" for p in parameters)})"

    def get_file_extension(self):
        return "php"
