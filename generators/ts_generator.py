from generators.code_generator import CodeGenerator


class TsCodeGenerator(CodeGenerator):
    """
    Generate Typescript code

    Parameters:
        syntax_tree: syntax_tree of the drawio file 
        file_path: path for the code files to be written to
        options: set of additional options
    """

    TYPE_MAPPINGS = {
        "boolean": "boolean",
        "bool": "boolean",
        "char": "string",
        "wchar": "string",
        "sbyte": "number",
        "int8": "number",
        "byte": "number",
        "uint8": "number",
        "short": "number",
        "int16": "number",
        "ushort": "number",
        "uint16": "number",
        "integer": "number",
        "int": "number",
        "int32": "number",
        "uint": "number",
        "uint32": "number",
        "long": "number",
        "int64": "number",
        "ulong": "number",
        "uint64": "number",
        "float": "number",
        "single": "number",
        "double": "number",
        "bigint": "bigint",
        "decimal": "number",
        "string": "string",
        "wstring": "wstring",
        "date": "Date",
        "time": "Date",
        "datetime": "Date",
        "timestamp": "Date",
    }

    def __init__(self, syntax_tree, file_path, options):
        CodeGenerator.__init__(self, syntax_tree, file_path, options)

    @staticmethod
    def _accessor_name(property_name):
        if property_name.startswith("_"):
            return property_name.lstrip('_')
        return property_name + "Property"

    @staticmethod
    def _parameter_name(property_name):
        return "arg" + property_name.strip('_').capitalize()

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

            for module, symbols in self._options['imports'].items():
                class_header += f"import {{ {', '.join(symbols)} }} from '{module}';\n"
                add_linebreak = True

            for baseclass in baseclasses:
                class_header += f"import {{ {baseclass} }} from './{baseclass}.ts';\n"
                add_linebreak = True

            for interface in interfaces:
                class_header += f"import {{ {interface} }} from './{interface}.ts';\n"
                add_linebreak = True

            for reference in references:
                class_header += f"import {{ {reference} }} from './{reference}.ts';\n"
                add_linebreak = True

            if add_linebreak:
                class_header += "\n"

        class_header += f"export {class_type} {class_name}"
        if len(baseclasses) > 0:
            class_header += f" extends {baseclasses[0]}"
        if len(interfaces) > 0:
            class_header += f" implements {', '.join(interfaces)}"
        class_header += " {\n"

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

        properties_string = ""
        property_prefix = ""
        first_prop = True

        if not is_enum and self._options['encapsulate_all_props']:
            property_prefix = "_"

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
                p = (f"\t{self._get_property_access(property_def)} {property_prefix}{property_def['name']}"
                     f": {self._map_type(property_def['type'])}")
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
            if self._get_property_access(property_def) == "private":
                property_name = property_def['name']
                if self._options['encapsulate_all_props']:
                    property_name = f"_{property_name}"

                accessor_name = self._accessor_name(property_name)
                accessor_type = self._map_type(property_def['type'])
                parameter_name = self._parameter_name(property_name)

                accessors_string += (f"\tpublic get {accessor_name}(): {accessor_type} {{\n"
                                     f"\t\treturn this.{property_name};\n\t}}\n\n")

                accessors_string += (f"\tpublic set {accessor_name}({parameter_name}: {accessor_type}) {{\n"
                                     f"\t\tthis.{property_name} = {parameter_name};\n\t}}\n\n")

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
                m = f"\t{method_def['name']}{params}: {self._map_type(method_def['return_type'])};"
            else:
                m = f"\t{method_def['access']} {method_def['name']}{params}: {self._map_type(method_def['return_type'])} {{\n\t}}"
            methods_string += m + "\n\n"

        if class_type in ("class", "abstract class"):
            for interface_method in interface_methods:
                params = self._get_parameter_list(interface_method['parameters'])
                m = f"\tpublic {interface_method['name']}{params}: {self._map_type(interface_method['return_type'])} {{\n\t}}"
                methods_string += m + "\n\n"

        return methods_string

    def _generate_default_ctor(self, class_name):
        return ""

    def _generate_full_arg_ctor(self, class_name, properties):
        prefix = ""
        if self._options['encapsulate_all_props']:
            prefix = "_"

        separator = ",\n\t\t\t" if len(properties) > 4 else ", "
        ctor_string = "\tpublic constructor("
        ctor_string += separator.join([f"{p['name']}: {self._map_type(p['type'])} = {self._default_value(p['type'])}"
                                       for p in properties.values()])
        ctor_string += ") {\n"
        ctor_string += '\n'.join([f"\t\tthis.{prefix}{p['name']} = {p['name']};" for p in properties.values()])
        ctor_string += "\n\t}\n\n"

        return ctor_string

    def _generate_equal_hashcode(self, class_name, properties):
        return ""

    def _generate_to_string(self, class_name, properties):
        method_string = "\tpublic toString(): string {\n"
        method_string += f"\t\treturn `{class_name} \\{{"
        method_string += ', '.join([f"{p['name']}=${{this.{p['name']}}}" for p in properties.values()])
        method_string += "\\}`;\n\t}\n\n"

        return method_string

    def _package_directive(self, package_name):
        return None

    def _map_type(self, typename):
        return self.TYPE_MAPPINGS.get(typename.lower(), typename)

    def _default_value(self, typename):
        typename = self._map_type(typename)
        if typename == "boolean":
            return "false"
        if typename in ("number", "bigint"):
            return "0"
        if typename == "string":
            return '""'
        return "null"

    def _get_parameter_list(self, param_types):
        _ndx = 0
        param_list = "("

        for param_type in param_types:
            if _ndx > 0:
                param_list += ", "
            param_list += f"arg{_ndx}: {param_type}"
            _ndx += 1

        param_list += ")"

        return param_list

    def _get_file_extension(self):
        return "ts"
