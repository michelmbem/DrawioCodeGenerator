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
        self.primary_keys = {}
        self.foreign_keys = {}
        self.tmp_primary_key = []
        self.tmp_foreign_keys = {}

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

                if not (class_def['type'] in ("class", "abstract class") and len(instance_props) > 0):
                    continue

                file_contents = self.generate_class_header(class_type, class_name, baseclasses)
                file_contents += self.generate_properties(class_type, class_name, instance_props, references)
                file_contents += f",\n\tconstraint pk_{class_name} primary key ({', '.join(self.tmp_primary_key)})"
                file_contents += self.generate_class_footer()

                self.files.append((class_name, file_contents))
                self.primary_keys[class_name] = self.tmp_primary_key
                self.foreign_keys[class_name] = self.tmp_foreign_keys
                self.tmp_primary_key = []
                self.tmp_foreign_keys = {}

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

        header_string = f"CREATE TABLE {class_name} (\n"

        if len(baseclasses) > 0:
            pk = self.get_primary_key(baseclasses[0])

            for p in pk:
                header_string += f"\t{p['name']} {self.map_type(p['type'])} not null,\n"

            self.tmp_primary_key = [p['name'] for p in pk]
            self.tmp_foreign_keys[baseclasses[0]] = (self.tmp_primary_key, True)

        return header_string

    def generate_class_footer(self, class_type = None):
        """
        Generate the class footer

        Parameters:
            class_type: type of class; 'class', 'abstract class', 'interface' or 'enum'

        Returns:
            properties_string: the closing brace of a class definition
        """

        return "\n);\n"

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
            constraints = property_def['constraints']

            if first_prop:
                first_prop = False
            else:
                properties_string += ",\n"

            p = f"\t{property_def['name']} {self.map_type(property_def['type'], constraints)}"

            if constraints.get('required'):
                p += " not null"

            if constraints.get('unique'):
                p += " unique"

            if constraints.get('pk'):
                self.tmp_primary_key.append(property_def['name'])
                if constraints.get('identity'):
                    p += f" {self.dialect.identity_spec()}".rstrip()

            if property_def['default_value'] and not constraints.get('identity'):
                p += f" default {property_def['default_value']}"

            properties_string += p

        if len(self.tmp_primary_key) <= 0:
            generated_id = ("id", "integer", {'pk': True, 'identity': True})
            generated_id_string = f"\t{generated_id[0]} {self.map_type(generated_id[1], generated_id[2])},\n"
            self.tmp_primary_key.append(generated_id[0])

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
                        fk_column_name = pk_column['name']
                    else:
                        fk_column_name = f"{fk_column_prefix}_{pk_column['name']}"

                    fk_columns.append(fk_column_name)
                    properties_string += f"\t{fk_column_name} {self.map_type(pk_column['type'])}"
            else:
                fk_column_name = f"{fk_column_prefix}_id"
                fk_columns.append(fk_column_name)
                properties_string += f"\t{fk_column_name} {self.map_type('integer')}"

            if reference[2]:
                properties_string += " not null"

            self.tmp_foreign_keys[reference[1]] = (fk_columns, reference[2])

        return generated_id_string + properties_string

    def package_directive(self, package_name):
        return f"use {self.split_package_name(package_name)[-1]};\n\n"

    def map_type(self, typename, constraints = None):
        mapped_type = self.dialect.map_type(typename, constraints)

        if constraints:
            length = constraints.get("length")
            if not length:
                size = constraints.get("size")
                if size:
                    length = size[1]

            if length:
                lparen, rparen = mapped_type.find('('), mapped_type.find(')')
                if 0 <= lparen < rparen:
                    return f"{mapped_type[:lparen]}({length}){mapped_type[rparen + 1:]}"

        return mapped_type

    def get_file_extension(self):
        return "sql"

    def write_package_directive(self, f):
        if self.options['package'] and self.dialect.multi_catalog:
            f.write(self.package_directive(self.options['package']))

    def write_foreign_keys(self, f):
        for table_name, foreign_keys in self.foreign_keys.items():
            for foreign_table, settings in foreign_keys.items():
                fk_name = f"fk_{table_name}_{foreign_table}"
                foreign_columns = ', '.join(self.primary_keys[foreign_table])
                f.write(f"alter table {table_name} add constraint {fk_name} foreign key ({', '.join(settings[0])})"
                        f" references {foreign_table} ({foreign_columns})")
                if settings[1]: f.write(" on delete cascade")
                f.write(";\n")
