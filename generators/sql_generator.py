import traceback

from operator import itemgetter
from os import path

from generators.code_generator import CodeGenerator
from generators.sql_dialect.sql_dialects import SQLDialects


class SqlCodeGenerator(CodeGenerator):
    """
    Generate SQL code

    Parameters:
        syntax_tree: syntax_tree of the drawio file
        file_path: path for the code files to be written to
        options: set of additional options
    """

    def __init__(self, syntax_tree, file_path, options):
        super().__init__(syntax_tree, file_path, options)
        self.dialect = SQLDialects.get(options['dialect'])
        self.custom_types = []
        self.primary_keys = {}
        self.foreign_keys = {}
        self.table_primary_key = []
        self.table_foreign_keys = {}
        self.table_constraints = []

    def generate_code(self):
        """
        Use the syntax tree to generate code files for the UML class diagrams
        """

        print("<<< GENERATING CODE FILES FROM SYNTAX TREE >>>")

        try:
            self.ensure_dir_exists(self.file_path)

            for class_def in self.syntax_tree.values():
                get_items = itemgetter("name", "type", "properties")
                class_name, class_type, properties = get_items(class_def)
                baseclasses, _, references = self.get_class_dependencies(class_def)
                instance_props = {k: p for k, p in properties.items() if not p['constraints'].get("static")}

                match class_type:
                    case "enum":
                        enum_declaration = self.dialect.enum_decl(class_def)
                        if enum_declaration.strip():
                            self.custom_types.append(enum_declaration)
                        continue
                    case "class" | "abstract class":
                        if self.get_stereotype(class_name) == "embeddable" or len(instance_props) <= 0:
                            continue

                        file_contents = self.generate_class_header(class_type, class_name, baseclasses)
                        file_contents += self.generate_properties(class_type, class_name, instance_props, references)
                        file_contents += (f",\n\tconstraint {self.dialect.escape(f"pk_{class_name}")} primary key"
                                          f" ({', '.join(self.table_primary_key)})")
                        file_contents += self.generate_class_footer(class_type, class_name)
                    case _:
                        continue

                self.files.append((class_name, file_contents))
                self.primary_keys[class_name] = self.table_primary_key
                self.foreign_keys[class_name] = self.table_foreign_keys
                self.table_primary_key = []
                self.table_foreign_keys = {}
                self.table_constraints = []

            self.generate_files()
        except Exception as e:
            print(f"{self.__class__.__name__}.generate_code ERROR: {e}")
            traceback.print_exception(e)

    def generate_files(self):
        """
        Write generated code to file

        Returns:
            boolean: True if successful, False if unsuccessful
        """

        print(f"<<< WRITING FILES TO {self.file_path} >>>")

        try:
            if self.options['single_script']:
                filename = self.options['filename']
                file_path = path.join(self.file_path, f"{filename}.{self.get_file_extension()}")

                with open(file_path, "w") as f:
                    self.write_package_directive(f)

                    if len(self.custom_types) > 0:
                        f.write("-- CUSTOM TYPES:\n\n")
                        self.write_custom_types(f)

                    f.write("-- TABLES:\n\n")
                    for table_name, table_def in self.files:
                        f.write(table_def)
                        f.write("\n")

                    f.write("-- FOREIGN KEYS:\n\n")
                    self.write_foreign_keys(f)
            else:
                for table_name, table_def in self.files:
                    file_path = path.join(self.file_path, f"{table_name}.{self.get_file_extension()}")
                    with open(file_path, "w") as f:
                        self.write_package_directive(f)
                        f.write(table_def)

                if len(self.custom_types) > 0:
                    file_path = path.join(self.file_path, f"_custom_types.{self.get_file_extension()}")
                    with open(file_path, "w") as f:
                        self.write_package_directive(f)
                        self.write_custom_types(f)

                file_path = path.join(self.file_path, f"_foreign_keys.{self.get_file_extension()}")
                with open(file_path, "w") as f:
                    self.write_package_directive(f)
                    self.write_foreign_keys(f)
        except Exception as e:
            print(f"{self.__class__.__name__}.generate_files ERROR: {e}")
            traceback.print_exception(e)

    def generate_class_header(self, class_type, class_name, baseclasses, interfaces = None, references = None):
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

        header_string = f"CREATE TABLE {self.dialect.escape(class_name)} (\n"

        if len(baseclasses) > 0:
            for pk_field in self.get_primary_key(baseclasses[0]):
                pk_field_name = self.dialect.escape(pk_field['name'])
                self.table_primary_key.append(pk_field_name)
                header_string += f"\t{pk_field_name} {self.map_type(pk_field['type'])} not null,\n"

            self.table_foreign_keys[baseclasses[0]] = (self.table_primary_key, True)

        return header_string

    def generate_class_footer(self, class_type, class_name):
        """
        Generate the class footer

        Parameters:
            class_type: type of class; 'class', 'abstract class', 'interface' or 'enum'
            class_name: name of class

        Returns:
            properties_string: the closing brace of a class definition
        """

        footer_string = ""
        count = {}

        for constraint in self.table_constraints:
            column_name = self.dialect.escape(constraint[1])
            match constraint[0]:
                case "unique":
                    constraint_name = self.dialect.escape(f"un_{class_name}_{constraint[1]}")
                    footer_string += f",\n\tconstraint {constraint_name} unique ({column_name})"
                case "check":
                    if constraint[1] in count:
                        count[constraint[1]] += 1
                    else:
                        count[constraint[1]] = 1

                    constraint_name = self.dialect.escape(f"ch_{class_name}_{constraint[1]}{count[constraint[1]]}")
                    footer_string += f",\n\tconstraint {constraint_name} check ({column_name} {constraint[2]})"

        footer_string += "\n);\n"

        return footer_string

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

        generated_id_string = ""
        properties_string = ""
        first_prop = True

        for property_def in properties.values():
            property_type = property_def['type']
            property_type_def = self.get_class_by_name(property_type)

            if first_prop:
                first_prop = False
            else:
                properties_string += ",\n"

            if property_type_def:
                property_type_props = property_type_def['properties'].values()

                if property_type_def['type'] == "enum":
                    p = f"\t{self.dialect.escape(property_def['name'])} {self.dialect.enum_spec(property_type, property_type_props)}"
                else:
                    p = ",\n".join(self.field_spec(p, f"{property_def['name']}_", property_def['constraints'])
                                   for p in property_type_props)
            else:
                p = self.field_spec(property_def, "", {})

            properties_string += p

        if len(self.table_primary_key) <= 0:
            generated_id = ("id", "integer", {'pk': True, 'identity': True})
            generated_id_string = f"\t{self.dialect.escape(generated_id[0])} {self.map_type(generated_id[1], generated_id[2])},\n"
            self.table_primary_key.append(generated_id[0])

        for reference in references:
            if reference[0] != "to": continue

            fk_columns = []
            fk_column_prefix = f"{reference[1][0].lower()}{reference[1][1:]}"
            pk_columns = self.get_primary_key(reference[1])

            if first_prop:
                first_prop = False
            else:
                properties_string += ",\n"

            if len(pk_columns) > 0:
                for pk_column in pk_columns:
                    if pk_column['name'].lower().startswith(reference[1].lower()):
                        fk_column_name = self.dialect.escape(pk_column['name'])
                    else:
                        fk_column_name = self.dialect.escape(f"{fk_column_prefix}_{pk_column['name']}")

                    fk_columns.append(fk_column_name)
                    properties_string += f"\t{fk_column_name} {self.map_type(pk_column['type'])}"
            else:
                fk_column_name = self.dialect.escape(f"{fk_column_prefix}_id")
                fk_columns.append(fk_column_name)
                properties_string += f"\t{fk_column_name} {self.map_type('integer')}"

            if reference[2]:
                properties_string += " not null"

            self.table_foreign_keys[reference[1]] = (fk_columns, reference[2])

        return generated_id_string + properties_string

    def package_directive(self, package_name):
        catalog_name = self.split_package_name(package_name)[-1]
        return self.dialect.catalog_switch_directive(catalog_name)

    def map_type(self, typename, constraints = None):
        mapped_type = self.dialect.map_type(typename, constraints)

        if constraints:
            size = constraints.get("size")
            if not size:
                size = constraints.get("length")
            if isinstance(size, list):
                lparen, rparen = mapped_type.find('('), mapped_type.find(')')
                if 0 <= lparen < rparen:
                    return f"{mapped_type[:lparen]}({size[-1]}){mapped_type[rparen + 1:]}"

        return mapped_type

    def get_file_extension(self):
        return "sql"

    def field_spec(self, property_def, prefix, group_constraints):
        constraints = property_def['constraints']
        property_name = property_def['name']

        field_name = self.dialect.escape(f"{prefix}{property_def['name']}")
        field_string = f"\t{field_name} {self.map_type(property_def['type'], constraints)}"

        if constraints.get('required') or group_constraints.get('required'):
            field_string += " not null"

        if constraints.get('pk'):
            self.table_primary_key.append(field_name)
            if constraints.get('identity'):
                field_string += f" {self.dialect.identity_spec()}".rstrip()

        if property_def['default_value'] and not constraints.get('identity'):
            field_string += f" default {property_def['default_value']}"

        if constraints.get('unique'):
            self.table_constraints.append(("unique", property_name))

        constraint = constraints.get('min')
        if isinstance(constraint, list):
            self.table_constraints.append(("check", property_name, f">= {constraint[0]}"))

        constraint = constraints.get('max')
        if isinstance(constraint, list):
            self.table_constraints.append(("check", property_name, f"<= {constraint[0]}"))

        constraint = constraints.get('range')
        if isinstance(constraint, list) and len(constraint) > 1:
            self.table_constraints.append(("check", property_name, f"between {constraint[0]} and {constraint[1]}"))

        return field_string

    def write_package_directive(self, f):
        if self.options['package'] and self.dialect.multi_catalog:
            f.write(self.package_directive(self.options['package']))

    def write_custom_types(self, f):
        for type_definition in self.custom_types:
            f.write(type_definition)

    def write_foreign_keys(self, f):
        for table_name, foreign_keys in self.foreign_keys.items():
            escaped_table_name = self.dialect.escape(table_name)
            for foreign_table, settings in foreign_keys.items():
                escaped_foreign_table = self.dialect.escape(foreign_table)
                fk_name = self.dialect.escape(f"fk_{table_name}_{foreign_table}")
                foreign_columns = ', '.join(self.primary_keys[foreign_table])
                f.write(f"alter table {escaped_table_name} add constraint {fk_name} foreign key ({', '.join(settings[0])})"
                        f" references {escaped_foreign_table} ({foreign_columns})")
                if settings[1]: f.write(" on delete cascade")
                f.write(";\n")
