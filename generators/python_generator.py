from generators.code_generator import CodeGenerator


class PythonCodeGenerator(CodeGenerator):
    """
    Generate Python code

    Parameters:
        syntax_tree: syntax_tree of the drawio file 
        file_path: path for the code files to be written to
        options: set of additional options
    """

    def __init__(self, syntax_tree, file_path, options):
        super().__init__(syntax_tree, file_path, options)

    @staticmethod
    def accessor_name(property_name):
        if property_name.startswith("_"):
            return property_name.lstrip('_')
        return property_name + "_property"

    @staticmethod
    def parameter_name(property_name):
        return "arg_" + property_name.lstrip('_')

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
        imports = set()

        if class_type == "enum":
            imports.add("from enum import Enum, auto")
            class_ancestors = "(Enum)"
        else:
            if class_type == "interface":
                imports.add("from abc import ABC, abstractmethod")

            for module, symbols in self.options['imports'].items():
                imports.add(f"from {module} import {', '.join(symbols)}")

            dependencies = {*baseclasses, *interfaces, *references}
            imports |= set(f"from {dependency} import {dependency}" for dependency in dependencies if dependency != class_name)

            class_ancestors = "("
            if class_type == "interface":
                class_ancestors += "ABC"
            if len(baseclasses) > 0:
                if class_type == "interface":
                    class_ancestors += ", "
                class_ancestors += ', '.join(baseclasses)
            if len(interfaces) > 0:
                if class_type == "interface" or len(baseclasses) > 0:
                    class_ancestors += ", "
                class_ancestors += ', '.join(interfaces)
            class_ancestors += ")"
            if class_ancestors == "()":
                class_ancestors = ""

        for import_line in sorted(imports):
            class_header += f"{import_line}\n"

        if len(imports) > 0:
            class_header += "\n\n"

        class_header += f"class {class_name}{class_ancestors}:\n"

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

        return ""

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
        property_prefix = ""
        counter = 0

        if not is_enum:
            for property_def in properties.values():
                if property_def['constraints'].get('static', False):
                    p = f"\t{property_def['name']} = "
                    if property_def['default_value']:
                        p += property_def['default_value']
                    else:
                        p += self.default_value(property_def['type'])
                    p += "\n"
                    properties_string += p

            properties_string += "\n\tdef __init__(self, *args, **kwargs):\n\t\targc = len(args)\n"

            if self.options['encapsulate_all_props']:
                property_prefix = "_"

        for property_def in properties.values():
            if is_enum:
                p = f"\t{property_def['name']} = "
                if property_def['default_value']:
                    p += property_def['default_value']
                else:
                    p += "auto()"
                p += "\n"
            else:
                if property_def['constraints'].get('static', False):
                    continue

                p = f"\n\t\tif argc > {counter}:\n"
                p += f"\t\t\tself.{property_prefix}{property_def['name']} = args[{counter}]\n"
                p += "\t\telse:\n"
                p += f"\t\t\tself.{property_prefix}{property_def['name']} = kwargs.get('{property_def['name']}', "
                if property_def['default_value']:
                    p += property_def['default_value']
                else:
                    p += self.default_value(property_def['type'])
                p += ")\n"

            properties_string += p
            counter += 1

        if not counter:
            properties_string = "\tdef __init__(self, *args, **kwargs):\n\t\tpass\n"

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
            if property_def['constraints'].get('static', False):
                continue

            if self.get_property_access(property_def) == "private":
                property_name = property_def['name']
                if self.options['encapsulate_all_props']:
                    property_name = f"_{property_name}"

                accessor_name = self.accessor_name(property_name)
                parameter_name = self.parameter_name(property_name)

                accessors_string += (f"\t@property\n\tdef {accessor_name}(self):\n"
                                     f"\t\treturn self.{property_name}\n\n")

                accessors_string += (f"\t@{accessor_name}.setter\n"
                                     f"\tdef {accessor_name}(self, {parameter_name}):\n"
                                     f"\t\tself.{property_name} = {parameter_name}\n\n")

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
        comment = "# Todo: implement this method!"

        for method_def in methods.values():
            params = self.get_parameter_list(method_def['parameters'])
            if class_type in ("interface", "abstract class"):
                m = f"\t@abstractmethod\n\tdef {method_def['name']}{params}:\n\t\tpass"
            else:
                m = ""
                if method_def['constraints'].get('static', False):
                    m += "\t@staticmethod\n"
                    params = f"({', '.join(p['name'] for p in method_def['parameters'])})"
                m += f"\tdef {method_def['name']}{params}:\n\t\t{comment}\n"
                if method_def['return_type'] == "void":
                    m += "\t\tpass"
                else:
                    m += f"\t\treturn {self.default_value(method_def['return_type'])}"
            methods_string += m + "\n\n"

        # inherited abstract methods
        if class_type in ("class", "abstract class"):
            for interface_method in interface_methods:
                params = self.get_parameter_list(interface_method['parameters'])
                m = f"\tdef {interface_method['name']}{params}:\n\t\t{comment}\n"
                if interface_method['return_type'] == "void":
                    m += "\t\tpass"
                else:
                    m += f"\t\treturn {self.default_value(interface_method['return_type'])}"
                methods_string += m + "\n\n"

        return methods_string

    def generate_equal_hashcode(self, class_name, properties, call_super):
        prefix = ""
        if self.options['encapsulate_all_props']:
            prefix = "_"

        method_string = "\tdef __members(self):\n"
        method_string += "\t\treturn ("
        method_string += ', '.join(f"self.{prefix}{p['name']}" for p in properties.values())
        method_string += ",)\n\n"

        method_string += "\tdef __eq__(self, other):\n"
        method_string += "\t\tif type(other) is type(self):\n"
        method_string += "\t\t\treturn self.__members() == other.__members()\n"
        method_string += "\t\treturn False\n\n"

        method_string += "\tdef __hash__(self):\n"
        method_string += "\t\treturn hash(self.__members())\n\n"

        return method_string

    def generate_to_string(self, class_name, properties, call_super):
        prefix = ""
        if self.options['encapsulate_all_props']:
            prefix = "_"

        method_string = "\tdef __str__(self):\n"
        method_string += f"\t\treturn f\"{class_name} {{{{"
        method_string += ', '.join(f"{p['name']}={{self.{prefix}{p['name']}}}" for p in properties.values())
        method_string += "}}\"\n\n"

        return method_string

    def default_value(self, typename):
        typename = typename.lower()
        if typename in ("boolean", "bool"):
            return "False"
        if typename in ("sbyte", "int8", "byte", "uint8", "short", "int16", "ushort", "uint16",
                        "integer", "int", "int32", "uint", "uint32", "long", "int64", "ulong",
                        "uint64", "float", "single", "double", "bigint", "decimal"):
            return "0"
        if typename in ("char", "wchar", "string", "wstring"):
            return '""'
        return "None"

    def get_parameter_list(self, parameters):
        return f"(self{''.join(f', {p['name']}' for p in parameters)})"

    def get_file_extension(self):
        return "py"
