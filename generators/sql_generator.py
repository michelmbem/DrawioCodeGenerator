import traceback

from generators.code_generator import CodeGenerator


class SqlCodeGenerator(CodeGenerator):
    """
    Generate SQL code

    Parameters:
        syntax_tree: syntax_tree of the drawio file 
        file_path: path for the code files to be written to
        options: set of additional options
    """

    TYPE_MAPPINGS = {
        "boolean": "bit",
        "bool": "bit",
        "char": "char(1)",
        "wchar": "nchar(1)",
        "sbyte": "tinyint",
        "int8": "tinyint",
        "byte": "tinyint",
        "uint8": "tinyint",
        "short": "smallint",
        "int16": "smallint",
        "ushort": "smallint",
        "uint16": "smallint",
        "integer": "int",
        "int": "int",
        "int32": "int",
        "uint": "int",
        "uint32": "int",
        "long": "bigint",
        "int64": "bigint",
        "ulong": "bigint",
        "uint64": "bigint",
        "float": "float(24)",
        "single": "float(24)",
        "double": "float(53)",
        "bigint": "decimal(30, 0)",
        "decimal": "decimal(30, 10)",
        "string": "varchar(2000)",
        "wstring": "nvarchar(2000)",
        "date": "date",
        "time": "time",
        "datetime": "datetime",
        "timestamp": "datetime",
    }

    def __init__(self, syntax_tree, file_path, options):
        CodeGenerator.__init__(self, syntax_tree, file_path, options)

    def generate_code(self):
        """
        Use the syntax tree to generate code files for the UML class diagrams
        """

        print("<<< GENERATING CODE FILES FROM SYNTAX TREE >>>")

        try:
            self._ensure_dir_exists(self._file_path)

            for class_def in self._syntax_tree.values():
                if class_def['type'] != "class":
                    continue

                file_contents = self._generate_class_header(class_def['type'], class_def['name'], None, None, None)
                file_contents += self._generate_properties(class_def['properties'], class_def['type'] == "enum")
                file_contents += self._generate_class_footer(class_def['type'], class_def['name'])

                self._files.append((class_def['name'], file_contents))

            self._generate_files()
        except Exception as e:
            print(f"{self.__class__.__name__}.generate_code ERROR: {e}")
            traceback.print_exception(e)

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
        if self._options['package']:
            class_header += self._package_directive(self._options['package'])
        class_header += f"CREATE TABLE {class_name} (\n"
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

        return "\n);\n"

    def _generate_properties(self, properties, _):
        """
        Generate properties for the class

        Parameters:
            properties: dictionary of properties
            _: ignored! should tell if we are generating enum members

        Returns:
            properties_string: string of the properties
        """

        properties_string = ""
        first_prop = True

        for property_def in properties.values():
            if first_prop:
                first_prop = False
            else:
                properties_string += ",\n"

            p = f"\t{property_def['name']} {self._map_type(property_def['type'])}"
            if property_def['default_value']:
                p += f" default {property_def['default_value']}"

            properties_string += p

        return properties_string

    def _generate_property_accessors(self, properties):
        return None

    def _generate_methods(self, methods, class_type, interface_methods):
        return None

    def _generate_default_ctor(self, class_name):
        return ""

    def _generate_full_arg_ctor(self, class_name, properties):
        return ""

    def _generate_equal_hashcode(self, class_name, properties):
        return ""

    def _generate_to_string(self, class_name, properties):
        return ""

    def _package_directive(self, package_name):
        return f"use {'_'.join(self._split_package_name(package_name))};\n\n"

    def _map_type(self, typename):
        return self.TYPE_MAPPINGS.get(typename.lower(), typename)

    def _default_value(self, typename):
        typename = typename.lower()
        if typename == "boolean":
            return "False"
        if typename in ("int8", "uint8", "int16", "uint16", "int32", "uint32",
                        "int64", "uint64", "single", "double", "bigint", "decimal"):
            return "0"
        if typename == "string":
            return '""'
        return "None"

    def _get_parameter_list(self, param_types):
        _ndx = 0
        param_list = "("

        for param_type in param_types:
            if _ndx > 0:
                param_list += ", "
            param_list += f"arg{_ndx} : {param_type}"
            _ndx += 1

        param_list += ")"

        return param_list

    def _get_file_extension(self):
        return "sql"
