from generators.code_generator import CodeGenerator


class JavaCodeGenerator(CodeGenerator):
    """
    Generate Java code

    Parameters:
        syntax_tree: syntax tree of the drawio file
        file_path: path for the code files to be written to
        options: set of additional options
    """

    TYPE_MAPPINGS = {
        "boolean": "boolean",
        "bool": "boolean",
        "char": "char",
        "wchar": "char",
        "sbyte": "byte",
        "int8": "byte",
        "byte": "byte",
        "uint8": "byte",
        "short": "short",
        "int16": "short",
        "ushort": "short",
        "uint16": "short",
        "integer": "int",
        "int": "int",
        "int32": "int",
        "uint": "int",
        "uint32": "int",
        "long": "long",
        "int64": "long",
        "ulong": "long",
        "uint64": "long",
        "float": "float",
        "single": "float",
        "double": "double",
        "bigint": "BigInteger",
        "decimal": "BigDecimal",
        "string": "String",
        "wstring": "String",
        "date": "LocalDate",
        "time": "LocalTime",
        "datetime": "LocalDateTime",
        "timestamp": "LocalDateTime",
        "unspecified": "Object",
    }

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

        class_header = ""

        if self.options['package']:
            class_header += self.package_directive(self.options['package'])

        if class_type != "enumeration":
            add_linebreak = False

            for module, symbols in self.options['imports'].items():
                for symbol in symbols:
                    class_header += f"import {module}.{symbol};\n"
                    add_linebreak = True

            if add_linebreak:
                class_header += "\n"

        class_header += f"public {class_type} {class_name}"
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
        first_prop = True

        for property_def in properties.values():
            if is_enum:
                if first_prop:
                    first_prop = False
                else:
                    properties_string += ",\n"

                p = f"\t{property_def['name']}"
                if property_def['default_value']:
                    p += f"({property_def['default_value']})"
            else:
                p = f"\t{self.get_property_access(property_def)} {self.map_type(property_def['type'])} {property_def['name']}"
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
            if self.get_property_access(property_def) == "private":
                getter = (f"\tpublic {self.map_type(property_def['type'])} get{property_def['name'].capitalize()}() {{\n"
                          f"\t\treturn {property_def['name']};\n\t}}\n\n")
                accessors_string += getter

                setter = (f"\tpublic void set{property_def['name'].capitalize()}({self.map_type(property_def['type'])} "
                          f"{property_def['name']}) {{\n\t\tthis.{property_def['name']} = {property_def['name']};\n\t}}\n\n")
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
                m = f"\t{self.map_type(method_def['return_type'])} {method_def['name']}{params};"
            else:
                m = f"\t{method_def['access']} {self.map_type(method_def['return_type'])} {method_def['name']}{params} {{\n"
                m += f"\t\t{comment}\n"
                if method_def['return_type'] != "void":
                    m += f"\t\treturn {self.default_value(method_def['return_type'])};\n"
                m += "\t}"

            methods_string += m + "\n\n"

        if class_type in ("class", "abstract class"):
            for interface_method in interface_methods:
                params = self.get_parameter_list(interface_method['parameters'])
                m = f"\tpublic {self.map_type(interface_method['return_type'])} {interface_method['name']}{params} {{\n"
                m += f"\t\t{comment}\n"
                if interface_method['return_type'] != "void":
                    m += f"\t\treturn {self.default_value(interface_method['return_type'])};\n"
                m += "\t}"
                methods_string += m + "\n\n"

        return methods_string

    def generate_default_ctor(self, class_name):
        return f"\tpublic {class_name}() {{\n\t}}\n\n"

    def generate_full_arg_ctor(self, class_name, properties):
        separator = ",\n\t\t\t" if len(properties) > 4 else ", "
        ctor_string = f"\tpublic {class_name}("
        ctor_string += separator.join([f"{self.map_type(p['type'])} {p['name']}" for p in properties.values()])
        ctor_string += ") {\n"
        ctor_string += '\n'.join([f"\t\tthis.{p['name']} = {p['name']};" for p in properties.values()])
        ctor_string += "\n\t}\n\n"

        return ctor_string

    def generate_equal_hashcode(self, class_name, properties):
        if len(properties) > 4:
            sep1 = " &&\n\t\t\t\t\t"
            sep2 = ",\n\t\t\t\t\t"
        else:
            sep1 = " && "
            sep2 = ", "

        method_string = "\t@Override\n\tpublic boolean equals(Object obj) {\n"
        method_string += "\t\tif (this == obj) return true;\n"
        method_string += f"\t\tif (obj instanceof {class_name} other) {{\n\t\t\treturn "
        method_string += sep1.join([f"Objects.equals({p['name']}, other.{p['name']})" for p in properties.values()])
        method_string += ";\n\t\t}\n\t\treturn false;\n\t}\n\n"

        method_string += "\t@Override\n\tpublic int hashCode() {\n"
        method_string += "\t\treturn Objects.hash("
        method_string += sep2.join([p['name'] for p in properties.values()])
        method_string += ");\n\t}\n\n"

        return method_string

    def generate_to_string(self, class_name, properties):
        sep1 = "\n\t\t\t" if len(properties) > 4 else ""
        sep2 = f".append(\", \"){sep1}"
        method_string = "\t@Override\n\tpublic String toString() {\n"
        method_string += f"\t\treturn new StringBuilder(\"{class_name} {{\"){sep1}"
        method_string += sep2.join([f".append(\"{p['name']}=\").append({p['name']})" for p in properties.values()])
        method_string += f"{sep1}.append(\"}}\").toString();\n\t}}\n\n"

        return method_string

    def package_directive(self, package_name):
        return f"package {'.'.join(self.split_package_name(package_name))};\n\n"

    def map_type(self, typename):
        return self.TYPE_MAPPINGS.get(typename.lower(), typename)

    def default_value(self, typename):
        typename = self.map_type(typename)
        if typename == "boolean":
            return "false"
        if typename == "char":
            return "'\\0'"
        if typename in ("byte", "short", "int", "long", "float", "double"):
            return "0"
        if typename == "String":
            return '""'
        return "null"

    def get_parameter_list(self, parameters):
        return '(' + ', '.join([f"{self.map_type(p['type'])} {p['name']}" for p in parameters]) + ')'

    def get_file_extension(self):
        return "java"
