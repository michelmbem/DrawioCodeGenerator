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
        "wstring": "string",
        "date": "Date",
        "time": "Date",
        "datetime": "Date",
        "timestamp": "Date",
        "uuid": "string",
        "guid": "string",
        "byte[]": "UInt8Array",
        "unspecified": "any",
    }

    def __init__(self, syntax_tree, file_path, options):
        super().__init__(syntax_tree, file_path, options)

    @staticmethod
    def accessor_name(property_name):
        if property_name.startswith("_"):
            return property_name.lstrip('_')
        return property_name + "Property"

    @staticmethod
    def parameter_name(property_name):
        return "arg" + property_name.strip('_').capitalize()

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
            imports = set()

            for module, symbols in self.options['imports'].items():
                imports.add(f"import {{ {', '.join(symbols)} }} from '{module}';")

            imports |= set(f"import {{ {baseclass} }} from './{baseclass}.ts';" for baseclass in baseclasses)
            imports |= set(f"import {{ {interface} }} from './{interface}.ts';" for interface in interfaces)
            imports |= set(f"import {{ {reference[1]} }} from './{reference[1]}.ts';" for reference in references if reference[1] != class_name)

            for import_line in sorted(imports):
                class_header += f"{import_line}\n"

            if len(imports) > 0:
                class_header += "\n"

        class_header += f"export {class_type} {class_name}"
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
 
    def generate_properties(self, class_type, class_name, properties, references):
        """
        Generate properties for the class

        Parameters:
            class_type: type of class; 'class', 'abstract class', 'interface' or 'enum'
            class_name: name of class
            properties: dictionary of properties
            references: the set of classes referenced by or referencing this class

        Returns:
            properties_string: string of the properties
        """

        properties_string = property_prefix = property_suffix = ""
        first_prop = True

        if class_type != "enum":
            if self.options['encapsulate_all_props']:
                property_prefix = "_"
            if self.options['optional_props']:
                property_suffix = "?"

        for property_def in properties.values():
            if class_type == "enum":
                if first_prop:
                    first_prop = False
                else:
                    properties_string += ",\n"

                p = f"\t{property_def['name']}"
                if property_def['default_value']:
                    p += f" = {property_def['default_value']}"
            else:
                modifier = f"{self.get_property_access(property_def)}"
                constraints = property_def['constraints']

                if constraints.get('static'):
                    modifier += " static"
                if constraints.get('final'):
                    modifier += " readonly"

                p = (f"\t{modifier} {property_prefix}{property_def['name']}{property_suffix}:"
                     f" {self.map_type(property_def['type'])}")
                if property_def['default_value']:
                    p += f" = {property_def['default_value']}"
                p += ";\n"

            properties_string += p

        for reference in references:
            field_name = f"_{reference[1][0].lower()}{reference[1][1:]}"

            match reference[0]:
                case "to":
                    properties_string += f"\tprivate {field_name}: {reference[1]};\n"
                case "from":
                    properties_string += f"\tprivate {field_name}s: {reference[1]}[] = [];\n"
                case _:
                    continue
 
        return properties_string

    def generate_property_accessors(self, class_name, properties, references):
        """
        Generate property accessors for the class

        Parameters:
            class_name: name of class
            properties: dictionary of properties
            references: the set of classes referenced by or referencing this class

        Returns:
            accessors_string: string of the property accessors
        """

        accessors_string = ""

        for property_def in properties.values():
            if self.get_property_access(property_def) == "private":
                property_name = property_def['name']
                if self.options['encapsulate_all_props']:
                    property_name = f"_{property_name}"

                param_ref_suffix = ""
                if self.options['optional_props']:
                    param_ref_suffix = "!"

                accessor_name = self.accessor_name(property_name)
                accessor_type = self.map_type(property_def['type'])
                parameter_name = self.parameter_name(property_name)
                constraints = property_def['constraints']

                target, modifier = "this", ""
                if constraints.get('static'):
                    target = class_name
                    modifier += " static"
                modifier += " "

                accessors_string += (f"\tpublic{modifier}get {accessor_name}(): {accessor_type} {{\n"
                                     f"\t\treturn {target}.{property_name}{param_ref_suffix};\n\t}}\n\n")

                if not constraints.get('final'):
                    accessors_string += (f"\tpublic{modifier}set {accessor_name}({parameter_name}: {accessor_type}) {{\n"
                                         f"\t\t{target}.{property_name} = {parameter_name};\n\t}}\n\n")

        for reference in references:
            field_name = f"_{reference[1][0].lower()}{reference[1][1:]}"
            field_type = reference[1]

            if reference[0] == "from":
                field_name += 's'
                field_type += "[]"

            accessor_name = self.accessor_name(field_name)
            parameter_name = self.parameter_name(field_name)

            match reference[0]:
                case "to" | "from":
                    accessors_string += (f"\tpublic get {accessor_name}(): {field_type} {{\n"
                                         f"\t\treturn this.{field_name};\n\t}}\n\n")

                    accessors_string += (f"\tpublic set {accessor_name}({parameter_name}: {field_type}) {{\n"
                                         f"\t\tthis.{field_name} = {parameter_name};\n\t}}\n\n")
                case _:
                    continue

        return accessors_string

    def generate_methods(self, class_type, methods, interface_methods):
        """
        Generate methods for the class

        Parameters:
            class_type: type of class; 'class', 'abstract class' or 'interface'
            methods: dictionary of methods
            interface_methods: methods of implemented interfaces
        
        Returns:
            methods_string: string of the methods 
        """
        
        methods_string = ""
        comment = "// Todo: implement this method!"

        for method_def in methods.values():
            params = self.get_parameter_list(method_def['parameters'])

            if class_type == "interface":
                m = f"\t{method_def['name']}{params}: {self.map_type(method_def['return_type'])};"
            else:
                constraints = method_def['constraints']

                modifier = ""
                if constraints.get('static'):
                    modifier += " static"
                elif constraints.get('abstract', False):
                    modifier += " abstract"
                modifier += " "

                m = f"\t{method_def['access']}{modifier}{method_def['name']}{params}: {self.map_type(method_def['return_type'])}"
                if constraints.get('abstract', False):
                    m += ";"
                else:
                    m += f" {{\n\t\t{comment}\n"
                    if method_def['return_type'] != "void":
                        m += f"\t\treturn {self.default_value(method_def['return_type'])};\n"
                    m += "\t}"

            methods_string += m + "\n\n"

        if class_type in ("class", "abstract class"):
            for interface_method in interface_methods:
                params = self.get_parameter_list(interface_method['parameters'])
                m = f"\tpublic {interface_method['name']}{params}: {self.map_type(interface_method['return_type'])} {{\n"
                m += f"\t\t{comment}\n"
                if interface_method['return_type'] != "void":
                    m += f"\t\treturn {self.default_value(interface_method['return_type'])};\n"
                m += "\t}"
                methods_string += m + "\n\n"

        return methods_string

    def generate_full_arg_ctor(self, class_name, baseclasses, properties, inherited_properties):
        prefix = ""
        if self.options['encapsulate_all_props']:
            prefix = "_"

        suffix = ""
        if not self.options['optional_props']:
            suffix = "!"

        separator = ",\n\t\t\t" if len(properties) + len(inherited_properties) > 4 else ", "
        ctor_string = "\tpublic constructor("
        if len(baseclasses) > 0:
            ctor_string += separator.join(f"{p['name']}?: {self.map_type(p['type'])}" for p in inherited_properties)
            if not ctor_string.endswith('(') and len(properties) > 0:
                ctor_string += ", "
        ctor_string += separator.join(f"{p['name']}?: {self.map_type(p['type'])}" for p in properties.values())
        ctor_string += ") {\n"
        if len(baseclasses) > 0:
            ctor_string += f"\t\tsuper({', '.join(p['name'] for p in inherited_properties)});\n"
        ctor_string += '\n'.join(f"\t\tthis.{prefix}{p['name']} = {p['name']}{suffix};" for p in properties.values())
        ctor_string += "\n\t}\n\n"

        return ctor_string

    def generate_to_string(self, class_name, baseclasses, properties):
        method_string = "\tpublic toString(): string {\n"
        method_string += f"\t\treturn `{class_name} \\{{"
        if len(baseclasses) > 0:
            method_string += "${super.toString()}"
            if len(properties) > 0:
                method_string += ", "
        method_string += ', '.join(f"{p['name']}=${{this.{p['name']}}}" for p in properties.values())
        method_string += "\\}`;\n\t}\n\n"

        return method_string

    def default_value(self, typename):
        typename = self.map_type(typename)
        if typename == "boolean":
            return "false"
        if typename in ("number", "bigint"):
            return "0"
        if typename == "string":
            return '""'
        if typename.endswith(']'):
            return "[]"
        return f"new {typename}()"

    def get_parameter_list(self, parameters):
        return f"({', '.join(f"{p['name']}: {self.map_type(p['type'])}" for p in parameters)})"

    def get_file_extension(self):
        return "ts"
