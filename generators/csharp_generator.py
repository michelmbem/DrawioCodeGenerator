from generators.code_generator import CodeGenerator


class CSharpCodeGenerator(CodeGenerator):
    """
    Generate C# code

    Parameters:
        syntax_tree: syntax tree of the drawio file
        file_path: path for the code files to be written to
        options: set of additional options
    """

    _TYPE_MAPPINGS = {
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
    }

    def __init__(self, syntax_tree, file_path, options):
        CodeGenerator.__init__(self, syntax_tree, file_path, options)

    @staticmethod
    def _accessor_name(property_name):
        if property_name[0].islower():
            return property_name.capitalize()
        return property_name + "Property"

    def _generate_class_header(self, class_type, class_name, baseclasses, interfaces, references):
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
            add_linebreak = False

            for module in self._options['imports'].keys():
                class_header += f"using {module};\n"
                add_linebreak = True

            if add_linebreak:
                class_header += "\n"

        if self._options['package']:
            class_header += self._package_directive(self._options['package'])

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

    def _generate_class_footer(self, class_type, class_name):
        """
        Generate the class footer

        Parameters:
            class_type: type of class; 'class', 'abstract class', 'interface' or 'enum'
            class_name: name of class

        Returns:
            properties_string: the closing brace of a class definition
        """

        return "}\n"
 
    def _generate_properties(self, properties, is_enum):
        """
        Generate properties for the class

        Parameters:
            properties: dictionary of properties
            is_enum: tells if we are generating enum members

        Returns:
            properties_string: string of the properties
        """

        if not is_enum and self._options['encapsulate_all_props']:
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
                p = f"\t{property_def['access']} {self._map_type(property_def['type'])} {property_def['name']}"
                if property_def['default_value']:
                    p += f" = {property_def['default_value']}"
                p += ";\n"

            properties_string += p
 
        return properties_string

    def _generate_property_accessors(self, properties):
        """
        Generate property accessors for the class

        Parameters:
            properties: dictionary of properties

        Returns:
            accessors_string: string of the property accessors
        """

        accessors_string = ""

        for property_def in properties.values():
            if self._options['encapsulate_all_props']:
                accessors_string += f"\tpublic {self._map_type(property_def['type'])} {property_def['name']} {{ get; set; }}\n\n"
            elif property_def['access'] == "private":
                accessor_pair = f"\tpublic {self._map_type(property_def['type'])} {self._accessor_name(property_def['name'])}\n\t{{"
                accessor_pair += f"\n\t\tget => {property_def['name']};"
                accessor_pair += f"\n\t\tset => {property_def['name']} = value;\n\t}}\n\n"
                accessors_string += accessor_pair

        return accessors_string

    def _generate_methods(self, methods, class_type, interface_methods):
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
            params = self._get_parameter_list(method_def['parameters'])
            if class_type == "interface":
                m = f"\t{self._map_type(method_def['return_type'])} {method_def['name']}{params};"
            else:
                m = f"\t{method_def['access']} {self._map_type(method_def['return_type'])} {method_def['name']}{params}\n\t{{\n"
                if method_def['return_type'] != "void":
                    m += f"\t\treturn {self._default_value(method_def['return_type'])};\n"
                m += "\t}"

            methods_string += m + "\n\n"

        if class_type in ("class", "abstract class"):
            for interface_method in interface_methods:
                params = self._get_parameter_list(interface_method['parameters'])
                m = f"\tpublic {self._map_type(interface_method['return_type'])} {interface_method['name']}{params}\n\t{{\n"
                if interface_method['return_type'] != "void":
                    m += f"\t\treturn {self._default_value(interface_method['return_type'])};\n"
                m += "\t}"
                methods_string += m + "\n\n"

        return methods_string

    def _generate_default_ctor(self, class_name):
        return f"\tpublic {class_name}()\n\t{{\n\t}}\n\n"

    def _generate_full_arg_ctor(self, class_name, properties):
        separator = ",\n\t\t\t" if len(properties) > 4 else ", "
        ctor_string = f"\tpublic {class_name}("
        ctor_string += separator.join([f"{self._map_type(p['type'])} {p['name']}" for p in properties.values()])
        ctor_string += ")\n\t{\n"
        ctor_string += '\n'.join([f"\t\tthis.{p['name']} = {p['name']};" for p in properties.values()])
        ctor_string += "\n\t}\n\n"

        return ctor_string

    def _generate_equal_hashcode(self, class_name, properties):
        method_string = "\tpublic override bool Equals(Object obj)\n\t{\n"
        method_string += "\t\tif (ReferenceEquals(this, obj)) return true;\n"
        method_string += f"\t\tif (obj is {class_name} other) {{\n\t\t\treturn "
        method_string += " &&\n\t\t\t\t".join([f"Equals({p['name']}, other.{p['name']})" for p in properties.values()])
        method_string += ";\n\t\t}\n\t\treturn false;\n\t}\n\n"

        method_string += "\tpublic override int GetHashCode()\n\t{\n"
        method_string += "\t\treturn HashCode.Combine("
        method_string += ', '.join([p['name'] for p in properties.values()])
        method_string += ");\n\t}\n\n"

        return method_string

    def _generate_to_string(self, class_name, properties):
        method_string = "\tpublic override string ToString() {\n"
        method_string += f"\t\treturn $\"{class_name} {{{{"
        method_string += ', '.join([f"{p['name']}={{{p['name']}}}" for p in properties.values()])
        method_string += "}}\";\n\t}\n\n"

        return method_string

    def _package_directive(self, package_name):
        return f"namespace {'.'.join(self._split_package_name(package_name))};\n\n"

    def _map_type(self, typename):
        return self._TYPE_MAPPINGS.get(typename.lower(), typename)

    def _default_value(self, typename):
        return f"default({self._map_type(typename)})"

    def _get_parameter_list(self, param_types):
        _ndx = 0
        param_list = "("

        for param_type in param_types:
            if _ndx > 0:
                param_list += ", "
            param_list += f"{param_type} arg{_ndx}"
            _ndx += 1

        param_list += ")"

        return param_list

    def _get_file_extension(self):
        return "cs"
