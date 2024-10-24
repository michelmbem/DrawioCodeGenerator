from generators.code_generator import CodeGenerator


class CppCodeGenerator(CodeGenerator):
    """
    Generate C++ code

    Parameters:
        syntax_tree: syntax tree of the drawio file
        file_path: path for the code files to be written to
        options: set of additional options
    """

    _TYPE_MAPPINGS = {
        "boolean": "bool",
        "bool": "bool",
        "char": "char",
        "wchar": "wchar_t",
        "sbyte": "signed char",
        "int8": "signed char",
        "byte": "unsigned char",
        "uint8": "unsigned char",
        "short": "short",
        "int16": "short",
        "ushort": "unsigned short",
        "uint16": "unsigned short",
        "integer": "int",
        "int": "int",
        "int32": "int",
        "uint": "unsigned int",
        "uint32": "unsigned int",
        "long": "long long",
        "int64": "long long",
        "ulong": "unsigned long long",
        "uint64": "unsigned long long",
        "float": "float",
        "single": "float",
        "double": "double",
        "string": "std::string",
        "wstring": "std::wstring",
        "date": "time_t",
        "time": "time_t",
        "datetime": "time_t",
        "timestamp": "time_t",
    }

    def __init__(self, syntax_tree, file_path, options):
        CodeGenerator.__init__(self, syntax_tree, file_path, options)

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

        class_header = "#pragma once\n\n"

        if class_type != "enum":
            add_linebreak = False

            for module in self._options['imports'].keys():
                class_header += f"#include {module}\n"
                add_linebreak = True

            for baseclass in baseclasses:
                class_header += f"#include \"{baseclass}.hpp\"\n"
                add_linebreak = True

            for interface in interfaces:
                class_header += f"#include \"{interface}.hpp\"\n"
                add_linebreak = True

            for reference in references:
                class_header += f"#include \"{reference}.hpp\"\n"
                add_linebreak = True

            if add_linebreak:
                class_header += "\n"

        if self._options['package']:
            class_header += self._package_directive(self._options['package'])
        else:
            class_header += "namespace __default__\n{\n"

        if class_type == "enum":
            type_of_class = "enum class"
        else:
            type_of_class = "class"

        class_header += f"\t{type_of_class} {class_name}"
        if len(baseclasses) > 0:
            class_header += f" : {', '.join([f"public {baseclass}" for baseclass in baseclasses])}"
        if len(interfaces) > 0:
            if len(baseclasses) > 0:
                class_header += ", "
            else:
                class_header += " : "
            class_header += ', '.join([f"public {interface}" for interface in interfaces])
        class_header += "\n\t{\n"

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

        if self._options['package']:
            braces = '}' * len(self._split_package_name(self._options['package']))
        else:
            braces = '}'

        return "\t};\n" + ''.join(braces)

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
        first_prop = True

        for property_def in properties.values():
            if is_enum:
                if first_prop:
                    first_prop = False
                else:
                    properties_string += ",\n"

                p = f"\t\t{property_def['name']}"
                if property_def['default_value']:
                    p += f" = {property_def['default_value']}"
            else:
                p = f"\t\t{self._get_property_access(property_def)}: {self._map_type(property_def['type'])} {property_def['name']}"
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
                getter = (f"\t\tpublic: {self._map_type(property_def['type'])} Get{property_def['name'].capitalize()}()"
                          f"\n\t\t{{\n\t\t\treturn {property_def['name']};\n\t\t}}\n\n")
                accessors_string += getter

                setter = (f"\t\tpublic: void Set{property_def['name'].capitalize()}({self._map_type(property_def['type'])}"
                          f" {property_def['name']})\n\t\t{{\n\t\t\tthis->{property_def['name']} = {property_def['name']};\n\t\t}}\n\n")
                accessors_string += setter

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
                m = f"\t\tpublic: virtual {self._map_type(method_def['return_type'])} {method_def['name']}{params} = 0;"
            else:
                m = f"\t\t{method_def['access']}: {self._map_type(method_def['return_type'])} {method_def['name']}{params}\n\t\t{{\n"
                if method_def['return_type'] != "void":
                    m += f"\t\t\treturn {self._default_value(method_def['return_type'])};\n"
                m += "\t\t}"

            methods_string += m + "\n\n"

        if class_type in ("class", "abstract class"):
            for interface_method in interface_methods:
                params = self._get_parameter_list(interface_method['parameters'])
                m = f"\t\tpublic: {self._map_type(interface_method['return_type'])} {interface_method['name']}{params} override\n\t\t{{\n"
                if interface_method['return_type'] != "void":
                    m += f"\t\t\treturn {self._default_value(interface_method['return_type'])};\n"
                m += "\t\t}"
                methods_string += m + "\n\n"

        return methods_string

    def _generate_default_ctor(self, class_name):
        return f"\t\tpublic: {class_name}()\n\t\t{{\n\t\t}}\n\n"

    def _generate_full_arg_ctor(self, class_name, properties):
        separator = ",\n\t\t\t\t" if len(properties) > 4 else ", "
        ctor_string = f"\t\tpublic: {class_name}("
        ctor_string += separator.join([f"{self._map_type(p['type'])} {p['name']}" for p in properties.values()])
        ctor_string += ")\n\t\t{\n"
        ctor_string += '\n'.join([f"\t\t\tthis->{p['name']} = {p['name']};" for p in properties.values()])
        ctor_string += "\n\t\t}\n\n"

        return ctor_string

    def _generate_equal_hashcode(self, class_name, properties):
        return ""

    def _generate_to_string(self, class_name, properties):
        return ""

    def _package_directive(self, package_name):
        return " { ".join([f"namespace {ns}" for ns in self._split_package_name(package_name)]) + "\n{\n"

    def _map_type(self, typename):
        return self._TYPE_MAPPINGS.get(typename.lower(), typename)

    def _default_value(self, typename):
        typename = self._map_type(typename)
        if typename == "bool":
            return "false"
        if typename == "char":
            return "'\\0'"
        if typename == "wchar_t":
            return "L'\\0'"
        if typename in ("signed char", "unsigned char", "short", "unsigned short", "int",
                        "unsigned int", "long long", "unsigned long long", "float", "double"):
            return "0"
        if typename == "std::string":
            return '""'
        if typename == "std::wstring":
            return 'L""'
        if typename.endswith("*"):
            return "nullptr"
        return f"{typename}()"

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
        return "hpp"
