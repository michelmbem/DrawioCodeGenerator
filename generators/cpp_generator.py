from generators.code_generator import CodeGenerator


class CppCodeGenerator(CodeGenerator):
    """
    Generate C++ code

    Parameters:
        syntax_tree: syntax tree of the drawio file
        file_path: path for the code files to be written to
        options: set of additional options
    """

    TYPE_MAPPINGS = {
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
        "bigint": {'std': "long long", 'boost': "cpp_int"},
        "decimal": {'std': "long double", 'boost': "cpp_dec_float_50"},
        "string": "string",
        "wstring": "wstring",
        "date": {'std': "time_t", 'boost': "date"},
        "time": {'std': "time_t", 'boost': "time_duration"},
        "datetime": {'std': "time_t", 'boost': "ptime"},
        "timestamp": {'std': "time_t", 'boost': "ptime"},
        "uuid": {'std': "array<char, 16>", 'boost': "uuid"},
        "guid": {'std': "array<char, 16>", 'boost': "uuid"},
        "unspecified": "int",
    }

    ACCESSORS_PREFIX = { 'pascal': ("Get", "Set", "Is", "To", "From", "Of") }
    ACCESSORS_PREFIX['camel'] = tuple(prefix.lower() for prefix in ACCESSORS_PREFIX['pascal'])
    ACCESSORS_PREFIX['snake'] = tuple(prefix + '_' for prefix in ACCESSORS_PREFIX['camel'])

    def __init__(self, syntax_tree, file_path, options):
        super().__init__(syntax_tree, file_path, options)
        self.current_class_name = None
        self.baseclass_name = None
        self.initializer_string = ""

    @staticmethod
    def accessor_name(property_name, naming_conv):
        if naming_conv != "snake" and property_name[0].islower():
            return f"{property_name[0].upper()}{property_name[1:]}"
        return property_name

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

        self.current_class_name = class_name
        class_header = "#pragma once\n\n"

        if class_type != "enum":
            header_files = set(self.options['imports'].keys())
            usings = set(symbol for symbols in self.options['imports'].values() for symbol in symbols if symbol)

            if self.options['use_boost']:
                boost_dependencies = self.get_boost_dependencies()
                header_files |= set(boost_dependencies.keys())
                usings |= set(symbol for symbols in boost_dependencies.values() for symbol in symbols if symbol)

            header_files |= set(f"\"{baseclass}.hpp\"" for baseclass in baseclasses)
            header_files |= set(f"\"{interface}.hpp\"" for interface in interfaces)
            header_files |= set(f"\"{reference[1]}.hpp\"" for reference in references if reference[1] != class_name)

            header_files = sorted(header_files)
            usings = sorted(usings)

            for header_file in header_files:
                if header_file.endswith('>'):
                    class_header += f"#include {header_file}\n"

            for header_file in header_files:
                if header_file.endswith('"'):
                    class_header += f"#include {header_file}\n"

            if len(header_files) > 0: class_header += "\n"

            for using in usings:
                if using.startswith("ns:"):
                    class_header += f"using namespace {using[3:]};\n"
                else:
                    class_header += f"using {using};\n"

            if len(usings) > 0: class_header += "\n"

        if self.options['package']:
            class_header += self.package_directive(self.options['package'])
        else:
            class_header += f"namespace __default__{self.lbrace()}\n"

        if class_type == "enum":
            type_of_class = "enum class"
        else:
            type_of_class = "class"

        class_header += f"\t{type_of_class} {class_name}"
        if len(baseclasses) > 0:
            self.baseclass_name = baseclasses[0]    # Note: check this
            class_header += f" : {', '.join(f"public {baseclass}" for baseclass in baseclasses)}"
        if len(interfaces) > 0:
            if self.baseclass_name:   # Checks if there is at least one baseclass
                class_header += ", "
            else:
                class_header += " : "
            class_header += ', '.join(f"public virtual {interface}" for interface in interfaces)
        class_header += f"{self.lbrace(1)}\n"

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

        self.baseclass_name = self.current_class_name = None

        if self.options['package']:
            braces = '}' * len(self.split_package_name(self.options['package']))
        else:
            braces = '}'

        footer_string = "\t};\n"
        if self.initializer_string:
            footer_string += "\n" + self.initializer_string
            self.initializer_string = ""
        footer_string += ''.join(braces)

        return footer_string

    def generate_properties(self, properties, is_enum, references):
        """
        Generate properties for the class

        Parameters:
            properties: dictionary of properties
            is_enum: tells if we are generating enum members
            references: the set of classes referenced by or referencing this class

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
                modifier = f"{self.get_property_access(property_def)}:"
                constraints = property_def['constraints']

                if constraints.get('static'):
                    modifier += " static"
                if constraints.get('final'):
                    modifier += " const"

                p = f"\t\t{modifier} {self.map_type(property_def['type'])} {property_def['name']}"
                if property_def['default_value']:
                    if constraints.get('static'):
                        self.initializer_string += "\t"
                        if constraints.get('final'):
                            self.initializer_string += "const "
                        self.initializer_string += f"{self.map_type(property_def['type'])} {self.current_class_name}::"
                        self.initializer_string += f"{property_def['name']}{{{property_def['default_value']}}};\n"
                    else:
                        p += f"{{{property_def['default_value']}}}"
                p += ";\n"

            properties_string += p

        for reference in references:
            field_name = f"{reference[1][0].lower()}{reference[1][1:]}"
            p = "\t\t"

            match reference[0]:
                case "to":
                    p += f"private: {reference[1]} {field_name};\n"
                case "from":
                    p += f"private: vector<{reference[1]}> {field_name}s;\n"
                case _:
                    continue

            properties_string += p

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
        lbrace = self.lbrace(2)
        prefix = self.ACCESSORS_PREFIX[self.options['naming']]

        for property_def in properties.values():
            if self.get_property_access(property_def) == "private":
                accessor_name = self.accessor_name(property_def['name'], self.options['naming'])
                accessor_type = self.map_type(property_def['type'])
                constraints = property_def['constraints']

                target, modifier = "this->", ""
                if constraints.get('static'):
                    target = f"{class_name}::"
                    modifier += " static"
                if constraints.get('final'):
                    modifier += " const"
                modifier += " "

                getter_prefix = prefix[2] if accessor_type == "bool" else prefix[0]
                getter = f"\t\tpublic:{modifier}{accessor_type} {getter_prefix}{accessor_name}()"
                if not constraints.get('static'):
                    getter += " const"
                getter += f"{lbrace}\n\t\t\treturn {property_def['name']};\n\t\t}}\n\n"
                accessors_string += getter

                if not constraints.get('final'):
                    setter = (f"\t\tpublic:{modifier}void {prefix[1]}{accessor_name}({accessor_type} {property_def['name']})"
                              f"{lbrace}\n\t\t\t{target}{property_def['name']} = {property_def['name']};\n\t\t}}\n\n")
                    accessors_string += setter

        for reference in references:
            field_name = f"{reference[1][0].lower()}{reference[1][1:]}"

            match reference[0]:
                case "to":
                    getter = (f"\t\tpublic: {reference[1]} {prefix[0]}{reference[1]}()"
                              f"{lbrace}\n\t\t\treturn {field_name};\n\t\t}}\n\n")
                    accessors_string += getter

                    setter = (f"\t\tpublic: void {prefix[1]}{reference[1]}({reference[1]} {field_name})"
                              f"{lbrace}\n\t\t\tthis->{field_name} = {field_name};\n\t\t}}\n\n")
                    accessors_string += setter
                case "from":
                    getter = (f"\t\tpublic: vector<{reference[1]}> {prefix[0]}{reference[1]}s()"
                              f"{lbrace}\n\t\t\treturn {field_name}s;\n\t\t}}\n\n")
                    accessors_string += getter

                    setter = (f"\t\tpublic: void {prefix[1]}{reference[1]}s(const vector<{reference[1]}>& {field_name}s)"
                              f"{lbrace}\n\t\t\tthis->{field_name}s = {field_name}s;\n\t\t}}\n\n")
                    accessors_string += setter
                case _:
                    continue

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
                m = f"\t\tpublic: virtual {self.map_type(method_def['return_type'])} {method_def['name']}{params} = 0;"
            else:
                constraints = method_def['constraints']

                modifier = ""
                if constraints.get('static'):
                    modifier += " static"
                elif constraints.get('abstract', False) or constraints.get('virtual', False):
                    modifier += " virtual"
                if constraints.get('final'):
                    modifier += " const"
                modifier += " "

                m = f"\t\t{method_def['access']}:{modifier}{self.map_type(method_def['return_type'])}"
                m += f" {method_def['name']}{params}"
                if constraints.get('abstract', False):
                    m += " = 0;"
                else:
                    m += f"\n\t\t{{\n\t\t\t{comment}\n"
                    if method_def['return_type'] != "void":
                        m += f"\t\t\treturn {self.default_value(method_def['return_type'])};\n"
                    m += "\t\t}"

            methods_string += m + "\n\n"

        if class_type in ("class", "abstract class"):
            for interface_method in interface_methods:
                params = self.get_parameter_list(interface_method['parameters'])
                m = f"\t\tpublic: {self.map_type(interface_method['return_type'])} {interface_method['name']}"
                m += f"{params} override\n\t\t{{\n\t\t\t{comment}\n"
                if interface_method['return_type'] != "void":
                    m += f"\t\t\treturn {self.default_value(interface_method['return_type'])};\n"
                m += "\t\t}"
                methods_string += m + "\n\n"

        return methods_string

    def generate_default_ctor(self, class_name, call_super):
        ctor_string = f"\t\tpublic: {class_name}()"
        if call_super:
            ctor_string += f": {self.baseclass_name}{{}}"
        ctor_string += f"{self.lbrace(2)}\n\t\t}}\n\n"

        return ctor_string

    def generate_full_arg_ctor(self, class_name, properties, call_super, inherited_properties):
        separator = ",\n\t\t\t\t" if len(properties) > 4 else ", "
        ctor_string = f"\t\tpublic: {class_name}("
        if call_super:
            ctor_string += separator.join(f"{self.map_type(p['type'])} {p['name']}" for p in inherited_properties)
            if not ctor_string.endswith('(') and len(properties) > 0:
                ctor_string += ", "
        ctor_string += separator.join(f"{self.map_type(p['type'])} {p['name']}" for p in properties.values())
        ctor_string += ")"
        if call_super:
            ctor_string += f":\n\t\t\t{self.baseclass_name}{{{', '.join(p['name'] for p in inherited_properties)}}}"
            if len(properties) > 0:
                ctor_string += ", "
        else:
            ctor_string += ":\n\t\t\t"
        ctor_string += ", ".join(f"{p['name']}{{{p['name']}}}" for p in properties.values())
        ctor_string += f"{self.lbrace(2)}\n\t\t}}\n\n"

        return ctor_string

    def package_directive(self, package_name):
        return " { ".join(f"namespace {ns}" for ns in self.split_package_name(package_name)) + self.lbrace() + "\n"

    def map_type(self, typename, constraints = None):
        mapped_type = super().map_type(typename, constraints)
        if isinstance(mapped_type, dict):
            key = "boost" if self.options['use_boost'] else "std"
            return mapped_type.get(key, "int")
        return mapped_type

    def default_value(self, typename):
        typename = self.map_type(typename)
        if typename == "bool":
            return "false"
        if typename == "char":
            return "'\\0'"
        if typename == "wchar_t":
            return "L'\\0'"
        if typename in ("signed char", "unsigned char", "short", "unsigned short", "int", "unsigned int",
                        "long long", "unsigned long long", "float", "double", "long double", "time_t"):
            return "0"
        if typename == "string":
            return '""'
        if typename == "wstring":
            return 'L""'
        if typename.endswith("*"):
            return "nullptr"
        if typename.endswith("]"):
            return "{}"
        return f"{typename}()"

    def get_parameter_list(self, parameters):
        return f"({', '.join(f"{self.map_type(p['type'])} {p['name']}" for p in parameters)})"

    def get_file_extension(self):
        return "hpp"

    def lbrace(self, tabs = 0):
        return " {" if self.options['lbrace_same_line'] else '\n' + '\t' * tabs + '{'

    def get_boost_dependencies(self):
        return {
            '<boost/multiprecision/cpp_int.hpp>': ["boost::multiprecision::cpp_int"],
            '<boost/multiprecision/cpp_dec_float.hpp>': ["boost::multiprecision::cpp_dec_float_50"],
            '<boost/date_time/gregorian/gregorian.hpp>': ["boost::gregorian::date"],
            '<boost/date_time/posix_time/posix_time.hpp>': ["boost::posix_time::time_duration", "boost::posix_time::ptime"],
            '<boost/uuid/uuid.hpp>': ["boost::uuids::uuid"]
        }
