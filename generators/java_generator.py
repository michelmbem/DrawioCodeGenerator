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
        "date": {'java8_local': "LocalDate", 'java8_offset': "LocalDate", 'sql_date': "Date", 'util_date': "Date", 'calendar': "Calendar"},
        "time": {'java8_local': "LocalTime", 'java8_offset': "OffsetTime", 'sql_date': "Time", 'util_date': "Date", 'calendar': "Calendar"},
        "datetime": {'java8_local': "LocalDateTime", 'java8_offset': "OffsetDateTime", 'sql_date': "Timestamp", 'util_date': "Date", 'calendar': "Calendar"},
        "timestamp": {'java8_local': "LocalDateTime", 'java8_offset': "OffsetDateTime", 'sql_date': "Timestamp", 'util_date': "Date", 'calendar': "Calendar"},
        "unspecified": "Object",
    }

    OBJECT_TYPE_MAPPINGS = {
        "boolean": "Boolean",
        "char": "Character",
        "byte": "Byte",
        "short": "Short",
        "int": "Integer",
        "long": "Long",
        "float": "Float",
        "double": "Double",
    }

    TEMPORAL_TYPE_IMPORTS = {
        "java8_local": {"package": "java.time", "classes": ["LocalDate", "LocalTime", "LocalDateTime"]},
        "java8_offset": {"package": "java.time", "classes": ["LocalDate", "OffsetTime", "OffsetDateTime"]},
        "sql_date": {"package": "java.sql", "classes": ["Date", "Time", "Timestamp"]},
        "util_date": {"package": "java.util", "classes": ["Date"]},
        "calendar": {"package": "java.util", "classes": ["Calendar"]},
    }

    def __init__(self, syntax_tree, file_path, options):
        super().__init__(syntax_tree, file_path, options)

    @staticmethod
    def accessor_name(property_name):
        if property_name[0].islower():
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

        class_header = ""

        if self.options['package']:
            class_header += self.package_directive(self.options['package'])

        if class_type != "enum":
            imports = set()

            for package, classes in self.options['imports'].items():
                for imported_class in classes:
                    imports.add(f"{package}.{imported_class}")

            temporal_type_imports = self.TEMPORAL_TYPE_IMPORTS[self.options['temporal_types']]
            for imported_class in temporal_type_imports['classes']:
                imports.add(f"{temporal_type_imports['package']}.{imported_class}")

            if class_type != "interface":
                for jpa_import in self.get_jpa_imports():
                    for imported_class in jpa_import['classes']:
                        imports.add(f"{jpa_import['package']}.{imported_class}")

                for imported_class in self.get_lombok_imported_classes():
                    imports.add(f"lombok.{imported_class}")

            for imported_class in sorted(imports):
                class_header += f"import {imported_class};\n"

            if len(imports) > 0:
                class_header += "\n"

        if class_type in ("class", "abstract class"):
            if self.options['add_jpa']:
                class_header += "@Entity\n"

            if self.options['use_lombok']:
                class_header += "@Data\n"
                if self.options['add_builder'] and class_type == "class":
                    class_header += "@Builder\n"
                if self.options['generate']['default_ctor']:
                    class_header += "@NoArgsConstructor\n"
                if self.options['generate']['full_arg_ctor']:
                    class_header += "@AllArgsConstructor\n"

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
                constraints = property_def['constraints']
                p = "\t"

                if not (constraints.get('static', False) or constraints.get('final', False)):
                    if self.options['add_jpa']:
                        if constraints.get('required', False):
                            p += "@NotNull\n\t"
                        if constraints.get('pk', False):
                            p += "@Id\n\t"
                        if constraints.get('identity', False):
                            p += "@GeneratedValue(strategy=GenerationType.IDENTITY)\n\t"
                        size = constraints.get('size')
                        if size:
                            p += f"@Size(min={size[0]},max={size[1]})\n\t"

                    if self.options['add_builder'] and property_def['default_value']:
                        p += "@Builder.Default\n\t"

                p += self.get_property_access(property_def)
                if constraints.get('static', False):
                    p += " static"
                if constraints.get('final', False):
                    p += " final"
                p += f" {self.map_type(property_def['type'], constraints)} {property_def['name']}"
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

        if self.options['use_lombok']:
            return ""

        accessors_string = ""

        for property_def in properties.values():
            if self.get_property_access(property_def) == "private":
                accessor_name = self.accessor_name(property_def['name'])
                accessor_type = self.map_type(property_def['type'])
                constraints = property_def['constraints']

                target, modifier = "this",  " "
                if constraints.get('static', False):
                    target, modifier = class_name, " static "

                getter = (f"\tpublic{modifier}{accessor_type} get{accessor_name}() {{\n"
                          f"\t\treturn {property_def['name']};\n\t}}\n\n")
                accessors_string += getter

                if not constraints.get('final', False):
                    setter = (f"\tpublic{modifier}void set{accessor_name}({accessor_type} {property_def['name']}) {{\n"
                              f"\t\t{target}.{property_def['name']} = {property_def['name']};\n\t}}\n\n")
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
                constraints = method_def['constraints']

                modifier = ""
                if constraints.get('static', False):
                    modifier += " static"
                elif constraints.get('final', False):
                    modifier += " final"
                modifier += " "

                m = f"\t{method_def['access']}{modifier}{self.map_type(method_def['return_type'])} {method_def['name']}{params} {{\n"
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

    def generate_default_ctor(self, class_name, call_super):
        if self.options['use_lombok']:
            return ""

        ctor_string = f"\tpublic {class_name}() {{\n"
        if call_super:
            ctor_string += "\t\tsuper();\n"
        ctor_string += "\t}\n\n"

        return ctor_string

    def generate_full_arg_ctor(self, class_name, properties, call_super, inherited_properties):
        if self.options['use_lombok']:
            return ""

        separator = ",\n\t\t\t" if len(properties) + len(inherited_properties) > 4 else ", "
        ctor_string = f"\tpublic {class_name}("
        if call_super:
            ctor_string += separator.join(f"{self.map_type(p['type'])} {p['name']}" for p in inherited_properties)
            if not ctor_string.endswith('(') and len(properties) > 0:
                ctor_string += ", "
        ctor_string += separator.join(f"{self.map_type(p['type'])} {p['name']}" for p in properties.values())
        ctor_string += ") {\n"
        if call_super:
            ctor_string += f"\t\tsuper({', '.join(p['name'] for p in inherited_properties)});\n"
        ctor_string += '\n'.join(f"\t\tthis.{p['name']} = {p['name']};" for p in properties.values())
        ctor_string += "\n\t}\n\n"

        return ctor_string

    def generate_equal_hashcode(self, class_name, properties, call_super):
        if self.options['use_lombok']:
            return ""

        if len(properties) > 2:
            sep1 = " &&\n\t\t\t\t\t"
            sep2 = ",\n\t\t\t\t\t"
        else:
            sep1 = " && "
            sep2 = ", "

        method_string = "\t@Override\n\tpublic boolean equals(Object obj) {\n"
        method_string += "\t\tif (this == obj) return true;\n"
        method_string += f"\t\tif (obj instanceof {class_name} other) {{\n\t\t\treturn "
        if call_super:
            method_string += "super.equals(other)"
            if len(properties) > 0:
                method_string += sep1
        method_string += sep1.join(f"Objects.equals({p['name']}, other.{p['name']})" for p in properties.values())
        method_string += ";\n\t\t}\n\t\treturn false;\n\t}\n\n"

        method_string += "\t@Override\n\tpublic int hashCode() {\n"
        method_string += "\t\treturn Objects.hash("
        if call_super:
            method_string += "super.hashCode()"
            if len(properties) > 0:
                method_string += sep2
        method_string += sep2.join(p['name'] for p in properties.values())
        method_string += ");\n\t}\n\n"

        return method_string

    def generate_to_string(self, class_name, properties, call_super):
        if self.options['use_lombok']:
            return ""

        sep1 = "\n\t\t\t" if len(properties) > 2 else ""
        sep2 = f".append(\", \"){sep1}"
        method_string = "\t@Override\n\tpublic String toString() {\n"
        method_string += f"\t\treturn new StringBuilder(\"{class_name} {{\"){sep1}"
        if call_super:
            method_string += ".append(super.toString())"
            if len(properties) > 0:
                method_string += sep2
            else:
                method_string += sep1
        method_string += sep2.join(f".append(\"{p['name']}=\").append({p['name']})" for p in properties.values())
        method_string += f"{sep1}.append(\"}}\").toString();\n\t}}\n\n"

        return method_string

    def package_directive(self, package_name):
        return f"package {'.'.join(self.split_package_name(package_name))};\n\n"

    def map_type(self, typename, constraints = None):
        mapped_type = super().map_type(typename, constraints)
        if isinstance(mapped_type, dict):
            return mapped_type.get(self.options['temporal_types'], "Object")
        if constraints and constraints.get("pk", False):
            return self.OBJECT_TYPE_MAPPINGS.get(mapped_type, mapped_type)
        return mapped_type

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
        return f"({', '.join(f"{self.map_type(p['type'])} {p['name']}" for p in parameters)})"

    def get_file_extension(self):
        return "java"

    def get_jpa_imports(self):
        jpa_imports = []

        if self.options['use_jakarta']:
            jee_root_package = "jakarta"
        else:
            jee_root_package = "javax"

        if self.options['add_jpa']:
            jpa_imports.append({
                "package": f"{jee_root_package}.persistence",
                "classes": ["Entity", "Id", "GeneratedValue", "GenerationType", "ManyToOne"]
            })
            jpa_imports.append({
                "package": f"{jee_root_package}.validation.constraints",
                "classes": ["NotNull", "Size"]
            })

        return jpa_imports

    def get_lombok_imported_classes(self):
        lombok_imported_classes = []

        if self.options['use_lombok']:
            lombok_imported_classes += ["Data"]
            if self.options['add_builder']:
                lombok_imported_classes += ["Builder"]
            if self.options['generate']['default_ctor']:
                lombok_imported_classes += ["NoArgsConstructor"]
            if self.options['generate']['full_arg_ctor']:
                lombok_imported_classes += ["AllArgsConstructor"]

        return lombok_imported_classes
