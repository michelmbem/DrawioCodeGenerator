from generators.code_generator import CodeGenerator


class CSharpCodeGenerator(CodeGenerator):
    """
    Generate C# code

    Parameters:
        syntax_tree: syntax tree of the drawio file
        file_path: path for the code files to be written to
        options: set of additional options
    """

    TYPE_MAPPINGS = {
        "boolean": "bool",
        "bool": "bool",
        "char": "char",
        "wchar": "char",
        "sbyte": "sbyte",
        "int8": "sbyte",
        "byte": "byte",
        "uint8": "byte",
        "short": "short",
        "int16": "short",
        "ushort": "ushort",
        "uint16": "ushort",
        "integer": "int",
        "int": "int",
        "int32": "int",
        "uint": "uint",
        "uint32": "uint",
        "long": "long",
        "int64": "long",
        "ulong": "ulong",
        "uint64": "ulong",
        "float": "float",
        "single": "float",
        "double": "double",
        "bigint": "BigInteger",
        "decimal": "decimal",
        "string": "string",
        "wstring": "string",
        "date": "DateTime",
        "time": "DateTime",
        "datetime": "DateTime",
        "timestamp": "DateTime",
        "unspecified": "object",
    }

    def __init__(self, syntax_tree, file_path, options):
        super().__init__(syntax_tree, file_path, options)

    @staticmethod
    def accessor_name(property_name, avoid_conflict):
        if property_name[0].islower():
            return f"{property_name[0].upper()}{property_name[1:]}"
        return property_name + "Property" if avoid_conflict else property_name

    @staticmethod
    def parameter_name(property_name):
        return f"{property_name[0].lower()}{property_name[1:]}"

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

        if class_type != "enum":
            usings = set(self.options['imports'].keys())

            if class_type != "interface" and self.options['add_efcore']:
                usings.add("System.Collections.Generic")
                usings.add("System.ComponentModel.DataAnnotations")
                usings.add("System.ComponentModel.DataAnnotations.Schema")

            for namespace in sorted(usings):
                class_header += f"using {namespace};\n"

            if len(usings) > 0:
                class_header += "\n"

        if self.options['package']:
            class_header += self.package_directive(self.options['package'])

        class_header += f"public {class_type} {class_name}"
        if len(baseclasses) > 0:
            class_header += f" : {baseclasses[0]}"
        if len(interfaces) > 0:
            if len(baseclasses) > 0:
                class_header += ", "
            else:
                class_header += " : "
            class_header += ', '.join(interfaces)
        class_header += "\n{\n"

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

        if not is_enum and self.options['encapsulate_all_props']:
            return ""

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
                modifier = self.get_property_access(property_def)
                constraints = property_def['constraints']

                if constraints.get('static', False):
                    if constraints.get('final', False):
                        modifier = f"{property_def['access']} const"
                    else:
                        modifier += " static"
                elif constraints.get('final', False):
                    modifier += " readonly"

                p = f"\t{modifier} {self.map_type(property_def['type'])} {property_def['name']}"
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
            constraints = property_def['constraints']
            modifier = " "

            if constraints.get('static', False):
                if constraints.get('final', False):
                    continue    # No encapsulation for constants
                modifier = " static "
            elif self.options['add_efcore']:
                if constraints.get('required', False):
                    accessors_string += "\t[Required]\n"
                if constraints.get('pk', False):
                    accessors_string += "\t[Key]\n"
                size = constraints.get('size')
                if size:
                    accessors_string += f"\t[MaxLength({size[1]})]\n"

            if self.options['encapsulate_all_props']:
                accessor_name = self.accessor_name(property_def['name'], False)
                accessors_string += f"\tpublic{modifier}{self.map_type(property_def['type'])} {accessor_name} {{ get;"
                if not constraints.get('final', False):
                    accessors_string += " set;"
                accessors_string += " }\n\n"
            elif property_def['access'] == "private":
                accessor_name = self.accessor_name(property_def['name'], True)
                accessors_string += f"\tpublic{modifier}{self.map_type(property_def['type'])} {accessor_name}\n\t{{"
                accessors_string += f"\n\t\tget => {property_def['name']};"
                if not constraints.get('final', False):
                    accessors_string += f"\n\t\tset => {property_def['name']} = value;"
                accessors_string += "\n\t}\n\n"

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
                constraints = method_def['constraints']

                modifier = ""
                if constraints.get('static', False):
                    modifier += " static"
                elif constraints.get('virtual', False):
                    modifier += " virtual"
                modifier += " "

                m = f"\t{method_def['access']}{modifier}{self.map_type(method_def['return_type'])} {method_def['name']}{params}\n\t{{\n"
                m += f"\t\t{comment}\n"
                if method_def['return_type'] != "void":
                    m += f"\t\treturn {self.default_value(method_def['return_type'])};\n"
                m += "\t}"

            methods_string += m + "\n\n"

        if class_type in ("class", "abstract class"):
            for interface_method in interface_methods:
                params = self.get_parameter_list(interface_method['parameters'])
                m = f"\tpublic {self.map_type(interface_method['return_type'])} {interface_method['name']}{params}\n\t{{\n"
                m += f"\t\t{comment}\n"
                if interface_method['return_type'] != "void":
                    m += f"\t\treturn {self.default_value(interface_method['return_type'])};\n"
                m += "\t}"
                methods_string += m + "\n\n"

        return methods_string

    def generate_default_ctor(self, class_name):
        return f"\tpublic {class_name}()\n\t{{\n\t}}\n\n"

    def generate_full_arg_ctor(self, class_name, properties):
        separator = ",\n\t\t\t" if len(properties) > 4 else ", "
        ctor_string = f"\tpublic {class_name}("
        ctor_string += separator.join(f"{self.map_type(p['type'])} {self.parameter_name(p['name'])}" for p in properties.values())
        ctor_string += ")\n\t{\n"
        ctor_string += '\n'.join(f"\t\tthis.{p['name']} = {self.parameter_name(p['name'])};" for p in properties.values())
        ctor_string += "\n\t}\n\n"

        return ctor_string

    def generate_equal_hashcode(self, class_name, properties):
        if len(properties) > 4:
            sep1 = " &&\n\t\t\t\t\t"
            sep2 = ",\n\t\t\t\t\t"
        else:
            sep1 = " && "
            sep2 = ", "

        method_string = "\tpublic override bool Equals(Object obj)\n\t{\n"
        method_string += "\t\tif (ReferenceEquals(this, obj)) return true;\n"
        method_string += f"\t\tif (obj is {class_name} other) {{\n\t\t\treturn "
        method_string += sep1.join(f"Equals({p['name']}, other.{p['name']})" for p in properties.values())
        method_string += ";\n\t\t}\n\t\treturn false;\n\t}\n\n"

        method_string += "\tpublic override int GetHashCode()\n\t{\n"
        method_string += "\t\treturn HashCode.Combine("
        method_string += sep2.join(p['name'] for p in properties.values())
        method_string += ");\n\t}\n\n"

        return method_string

    def generate_to_string(self, class_name, properties):
        method_string = "\tpublic override string ToString() {\n"
        method_string += f"\t\treturn $\"{class_name} {{{{"
        method_string += ', '.join(f"{p['name']}={{{p['name']}}}" for p in properties.values())
        method_string += "}}\";\n\t}\n\n"

        return method_string

    def package_directive(self, package_name):
        return f"namespace {'.'.join(self.split_package_name(package_name))};\n\n"

    def default_value(self, typename):
        return f"default({self.map_type(typename)})"

    def get_parameter_list(self, parameters):
        return f"({', '.join(f"{self.map_type(p['type'])} {self.parameter_name(p['name'])}" for p in parameters)})"

    def get_file_extension(self):
        return "cs"
