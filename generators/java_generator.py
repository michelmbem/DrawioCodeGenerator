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
        "uuid": "UUID",
        "guid": "UUID",
        "byte[]": "byte[]",
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

    @staticmethod
    def foreign_key_name(class_name, property_name):
        fk_name = property_name
        if not fk_name.lower().startswith(class_name.lower()):
            fk_name = f"{class_name[0].lower()}{class_name[1:]}_{fk_name}"
        return fk_name

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
        handle_jpa_inheritance = False

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

                if self.options['add_jpa'] and len(baseclasses) > 0:
                    handle_jpa_inheritance = True
                    jee_root_package = "jakarta" if self.options['use_jakarta'] else "javax"
                    imports.add(f"{jee_root_package}.persistence.PrimaryKeyJoinColumn")

            for imported_class in sorted(imports):
                class_header += f"import {imported_class};\n"

            if len(imports) > 0:
                class_header += "\n"

        if class_type in ("class", "abstract class"):
            if self.options['add_jpa']:
                if self.get_stereotype(class_name) == "embeddable":
                    class_header += "@Embeddable\n"
                else:
                    class_header += "@Entity\n"

                if handle_jpa_inheritance:
                    pk = self.get_primary_key(baseclasses[0])
                    pk = pk[0]['name'] if len(pk) > 0 else "--no-primary-key-found--"
                    class_header += f"@PrimaryKeyJoinColumn(name = \"{pk}\")\n"

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

        properties_string = ""
        first_prop = True
        add_jpa = self.options['add_jpa']
        add_builder = self.options['add_builder']

        for property_def in properties.values():
            if class_type == "enum":
                if first_prop:
                    first_prop = False
                else:
                    properties_string += ",\n"

                p = f"\t{property_def['name']}"
                if property_def['default_value']:
                    p += f"({property_def['default_value']})"
            else:
                data_type = property_def['type']
                constraints = property_def['constraints']
                p = "\t"

                if not (constraints.get('static') or constraints.get('final')):
                    if add_jpa:
                        p += self.get_data_annotations(data_type, constraints)
                    if add_builder and property_def['default_value']:
                        p += "@Builder.Default\n\t"

                p += self.get_property_access(property_def)
                if constraints.get('static'):
                    p += " static"
                if constraints.get('final'):
                    p += " final"
                p += f" {self.map_type(data_type, constraints)} {property_def['name']}"
                if property_def['default_value']:
                    p += f" = {property_def['default_value']}"
                p += ";\n"

            properties_string += p

        for reference in references:
            field_name = f"{reference[1][0].lower()}{reference[1][1:]}"
            inverse_field_name = f"{class_name[0].lower()}{class_name[1:]}"
            p = "\t"

            match reference[0]:
                case "to":
                    if add_jpa:
                        pk = self.get_primary_key(reference[1])
                        pk_len = len(pk)

                        p += "@ManyToOne\n\t"

                        if pk_len > 1:
                            p += "@JoinColumns({"
                            p += ','.join(f"\n\t\t@JoinColumn(name=\"{self.foreign_key_name(reference[1], p['name'])}\""
                                          f" referencedColumnName=\"{p['name']}\")" for p in pk)
                            p += "\n\t})\n\t"
                        else:
                            pk_field_name = pk[0]['name'] if pk_len > 0 else "id"
                            p += (f"@JoinColumn(name=\"{self.foreign_key_name(reference[1], pk_field_name)}\""
                                  f" referencedColumnName=\"{pk_field_name}\")\n\t")

                    p += f"private {reference[1]} {field_name};\n"
                case "from":
                    if add_jpa:
                        p += f"@OneToMany(mappedBy=\"{inverse_field_name}\""
                        if reference[2]:
                            p += ", cascade=CascadeType.ALL, orphanRemoval=true"
                        p += ")\n\t"
                    if add_builder:
                        p += "@Builder.Default\n\t"
                    p += f"private Set<{reference[1]}> {field_name}s = new HashSet<>();\n"
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

        if self.options['use_lombok']:
            return ""

        accessors_string = ""

        for property_def in properties.values():
            if self.get_property_access(property_def) == "private":
                accessor_name = self.accessor_name(property_def['name'])
                accessor_type = self.map_type(property_def['type'])
                constraints = property_def['constraints']

                target, modifier = "this",  " "
                if constraints.get('static'):
                    target, modifier = class_name, " static "

                getter_prefix = "is" if accessor_type == "boolean" else "get"
                getter = (f"\tpublic{modifier}{accessor_type} {getter_prefix}{accessor_name}() {{\n"
                          f"\t\treturn {property_def['name']};\n\t}}\n\n")
                accessors_string += getter

                if not constraints.get('final'):
                    setter = (f"\tpublic{modifier}void set{accessor_name}({accessor_type} {property_def['name']}) {{\n"
                              f"\t\t{target}.{property_def['name']} = {property_def['name']};\n\t}}\n\n")
                    accessors_string += setter

        for reference in references:
            field_name = f"{reference[1][0].lower()}{reference[1][1:]}"

            match reference[0]:
                case "to":
                    getter = (f"\tpublic {reference[1]} get{reference[1]}() {{\n"
                              f"\t\treturn {field_name};\n\t}}\n\n")
                    accessors_string += getter

                    setter = (f"\tpublic void set{reference[1]}({reference[1]} {field_name}) {{\n"
                              f"\t\tthis.{field_name} = {field_name};\n\t}}\n\n")
                    accessors_string += setter
                case "from":
                    getter = (f"\tpublic Set<{reference[1]}> get{reference[1]}s() {{\n"
                              f"\t\treturn {field_name}s;\n\t}}\n\n")
                    accessors_string += getter

                    setter = (f"\tpublic void set{reference[1]}s(Set<{reference[1]}> {field_name}s) {{\n"
                              f"\t\tthis.{field_name}s = {field_name}s;\n\t}}\n\n")
                    accessors_string += setter
                case _:
                    continue

        return accessors_string

    def generate_methods(self, class_type, methods, interface_methods):
        """
        Generate methods for the class

        Parameters:
            class_type: type of class; 'class', 'abstract class', 'interface' or 'enum'
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
                m = f"\t{self.map_type(method_def['return_type'])} {method_def['name']}{params};"
            else:
                constraints = method_def['constraints']

                modifier = ""
                if constraints.get('static'):
                    modifier += " static"
                elif constraints.get('abstract', False):
                    modifier += " abstract"
                elif constraints.get('final'):
                    modifier += " final"
                modifier += " "

                m = f"\t{method_def['access']}{modifier}{self.map_type(method_def['return_type'])} {method_def['name']}{params}"
                if constraints.get('abstract', False):
                    m += ";\n"
                else:
                    m += f" {{\n\t\t{comment}\n"
                    if method_def['return_type'] != "void":
                        m += f"\t\treturn {self.default_value(method_def['return_type'])};\n"
                    m += "\t}"

            methods_string += m + "\n\n"

        if class_type in ("class", "abstract class"):
            for interface_method in interface_methods:
                params = self.get_parameter_list(interface_method['parameters'])
                m = "\t@Override\n"
                m += f"\tpublic {self.map_type(interface_method['return_type'])} {interface_method['name']}{params} {{\n"
                m += f"\t\t{comment}\n"
                if interface_method['return_type'] != "void":
                    m += f"\t\treturn {self.default_value(interface_method['return_type'])};\n"
                m += "\t}"
                methods_string += m + "\n\n"

        return methods_string

    def generate_default_ctor(self, class_name, baseclasses):
        if self.options['use_lombok']:
            return ""

        ctor_string = f"\tpublic {class_name}() {{\n"
        if len(baseclasses) > 0:
            ctor_string += "\t\tsuper();\n"
        ctor_string += "\t}\n\n"

        return ctor_string

    def generate_full_arg_ctor(self, class_name, baseclasses, properties, inherited_properties):
        if self.options['use_lombok']:
            return ""

        separator = ",\n\t\t\t" if len(properties) + len(inherited_properties) > 4 else ", "
        ctor_string = f"\tpublic {class_name}("
        if len(baseclasses) > 0:
            ctor_string += separator.join(f"{self.map_type(p['type'])} {p['name']}" for p in inherited_properties)
            if not ctor_string.endswith('(') and len(properties) > 0:
                ctor_string += ", "
        ctor_string += separator.join(f"{self.map_type(p['type'])} {p['name']}" for p in properties.values())
        ctor_string += ") {\n"
        if len(baseclasses) > 0:
            ctor_string += f"\t\tsuper({', '.join(p['name'] for p in inherited_properties)});\n"
        ctor_string += '\n'.join(f"\t\tthis.{p['name']} = {p['name']};" for p in properties.values())
        ctor_string += "\n\t}\n\n"

        return ctor_string

    def generate_equal_hashcode(self, class_name, baseclasses, properties):
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
        if len(baseclasses) > 0:
            method_string += "super.equals(other)"
            if len(properties) > 0:
                method_string += sep1
        method_string += sep1.join(f"Objects.equals({p['name']}, other.{p['name']})" for p in properties.values())
        method_string += ";\n\t\t}\n\t\treturn false;\n\t}\n\n"

        method_string += "\t@Override\n\tpublic int hashCode() {\n"
        method_string += "\t\treturn Objects.hash("
        if len(baseclasses) > 0:
            method_string += "super.hashCode()"
            if len(properties) > 0:
                method_string += sep2
        method_string += sep2.join(p['name'] for p in properties.values())
        method_string += ");\n\t}\n\n"

        return method_string

    def generate_to_string(self, class_name, baseclasses, properties):
        if self.options['use_lombok']:
            return ""

        sep1 = "\n\t\t\t" if len(properties) > 2 else ""
        sep2 = f".append(\", \"){sep1}"
        method_string = "\t@Override\n\tpublic String toString() {\n"
        method_string += f"\t\treturn new StringBuilder(\"{class_name} {{\"){sep1}"
        if len(baseclasses) > 0:
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
        if self.options['add_jpa'] and constraints and constraints.get("pk", False):
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
            jpa_imports.append({"package": f"{jee_root_package}.persistence", "classes": ["*"]})
            jpa_imports.append({"package": f"{jee_root_package}.validation.constraints", "classes": ["*"]})
            jpa_imports.append({"package": "org.hibernate.validator.constraints", "classes": ["*"]})
            jpa_imports.append({"package": "org.hibernate.annotations", "classes": ["Generated"]})
            jpa_imports.append({"package": "org.hibernate.generator", "classes": ["EventType"]})

        return jpa_imports

    def get_lombok_imported_classes(self):
        lombok_imported_classes = []

        if self.options['use_lombok']:
            lombok_imported_classes.append("Data")
            if self.options['add_builder']:
                lombok_imported_classes.append("Builder")
            if self.options['generate']['default_ctor']:
                lombok_imported_classes.append("NoArgsConstructor")
            if self.options['generate']['full_arg_ctor']:
                lombok_imported_classes.append("AllArgsConstructor")

        return lombok_imported_classes

    def get_data_annotations(self, data_type, constraints):
        annotation_string = ""

        if data_type in self.defined_types:
            if self.syntax_tree[self.defined_types[data_type]]['type'] == "enum":
                annotation_string += "@Enumerated(EnumType.STRING)\n\t"
            else:
                annotation_string += "@Embedded\n\t"

        if constraints.get('required'):
            annotation_string += "@NotNull\n\t"

        if constraints.get('pk'):
            annotation_string += "@Id\n\t"

        if constraints.get('identity'):
            annotation_string += "@GeneratedValue(strategy=GenerationType.IDENTITY)\n\t"
        elif constraints.get('generated'):
            annotation_string += "@Generated(event={EventType.INSERT})\n\t"

        if constraints.get('lob'):
            annotation_string += "@Lob\n\t"

        if constraints.get('rowversion'):
            annotation_string += "@Version\n\t"

        constraint = constraints.get('min')
        if isinstance(constraint, list):
            annotation_string += f"@Min({constraint[0]})\n\t"

        constraint = constraints.get('max')
        if isinstance(constraint, list):
            annotation_string += f"@Max({constraint[0]})\n\t"

        constraint = constraints.get('range')
        if isinstance(constraint, list):
            if len(constraint) > 1:
                annotation_string += f"@Range(min={constraint[0]}, max={constraint[1]})\n\t"
            else:
                annotation_string += f"@Max({constraint[0]})\n\t"

        constraint = constraints.get('size')
        if isinstance(constraint, list):
            if len(constraint) > 1:
                annotation_string += f"@Size(min={constraint[0]}, max={constraint[1]})\n\t"
            else:
                annotation_string += f"@Size(max={constraint[0]})\n\t"
        else:
            constraint = constraints.get('length')
            if isinstance(constraint, list):
                annotation_string += f"@Size(max={constraint[0]})\n\t"

        match constraints.get('format', [""])[0].lower():
            case "date":
                annotation_string += "@Temporal(TemporalType.DATE)\n\t"
            case "time":
                annotation_string += "@Temporal(TemporalType.TIME)\n\t"
            case "datetime":
                annotation_string += "@Temporal(TemporalType.TIMESTAMP)\n\t"
            case "phone":
                annotation_string += r'@Pattern(regexp="^(((\\+|00)[1-9]+)[ -]?)?((\\(\\d+\\))|\\d)([ -]?\\d)+$")' + "\n\t"
            case "email":
                annotation_string += "@Email\n\t"
            case "url":
                annotation_string += "@URL\n\t"
            case "creditcard":
                annotation_string += "@CreditCardNumber\n\t"

        return annotation_string
