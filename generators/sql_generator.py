import traceback

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
        self.dialect = SQLDialects.get(options.get('dialect', "ansi"))
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
                baseclasses, _, __ = self.get_class_dependencies(class_def)
                instance_props = {k: p for k, p in class_def['properties'].items() if not p['constraints'].get("static", False)}

                if not (class_def['type'] in ("class", "abstract class") and len(instance_props) > 0):
                    continue

                class_name = class_def['name']
                file_contents = self.generate_class_header(None, class_name, baseclasses)
                file_contents += self.generate_properties(instance_props)
                if len(self.tmp_primary_key) > 0:
                    file_contents += f",\n\tconstraint pk_{class_name} primary key ({', '.join(self.tmp_primary_key)})"
                file_contents += self.generate_class_footer(None, class_name)

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
                header_string += f"\t{p['name']} {self.map_type(p['type'])},\n"

            self.tmp_primary_key = self.tmp_foreign_keys[baseclasses[0]] = [p['name'] for p in pk]

        return header_string

    def generate_class_footer(self, class_type = None, class_name = None):
        """
        Generate the class footer

        Parameters:
            class_type: type of class; 'class', 'abstract class', 'interface' or 'enum'
            class_name: name of class

        Returns:
            properties_string: the closing brace of a class definition
        """

        return "\n);\n"

    def generate_properties(self, properties, is_enum = False):
        """
        Generate properties for the class

        Parameters:
            properties: dictionary of properties
            is_enum: ignored! should tell if we are generating enum members

        Returns:
            properties_string: string of the properties
        """

        properties_string = ""
        first_prop = True

        for property_def in properties.values():
            constraints = property_def['constraints']
            is_identity = False

            if first_prop:
                first_prop = False
            else:
                properties_string += ",\n"

            p = f"\t{property_def['name']} {self.map_type(property_def['type'], constraints)}"

            if constraints.get('required', False):
                p += " not null"
            if constraints.get('unique', False):
                p += " unique"
            if constraints.get('identity', False):
                is_identity = True
                p += f" {self.dialect.identity_spec()}".rstrip()
            if constraints.get('pk', False):
                self.tmp_primary_key.append(property_def['name'])
            if constraints.get('fk', False):
                fk_target = constraints['fk_target']
                if fk_target in self.tmp_foreign_keys:
                    self.tmp_foreign_keys[fk_target].append(property_def['name'])
                else:
                    self.tmp_foreign_keys[fk_target] = [property_def['name']]

            if property_def['default_value'] and not is_identity:
                p += f" default {property_def['default_value']}"

            properties_string += p

        return properties_string

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
            for foreign_table, columns in foreign_keys.items():
                fk_name = f"fk_{table_name}_{foreign_table}"
                foreign_columns = ', '.join(self.primary_keys[foreign_table])
                f.write(f"alter table {table_name} add constraint {fk_name} foreign key ({', '.join(columns)})"
                        f" references {foreign_table} ({foreign_columns});\n")
