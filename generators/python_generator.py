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
        CodeGenerator.__init__(self, syntax_tree, file_path, options)

    @staticmethod
    def _accessor_name(property_name):
        if property_name.startswith("_"):
            return property_name.lstrip('_')
        return property_name + "_property"

    @staticmethod
    def _parameter_name(property_name):
        return "arg_" + property_name.lstrip('_')

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
        add_linebreaks = False

        if class_type == "enum":
            class_header += "from enum import Enum, auto\n"
            class_ancestors = "(Enum)"
            add_linebreaks = True
        else:
            if class_type == "interface":
                class_header += "from abc import ABC, abstractmethod\n"
                add_linebreaks = True

            for module, symbols in self._options['imports'].items():
                class_header += f"from {module} import {', '.join(symbols)}\n"
                add_linebreaks = True

            for baseclass in baseclasses:
                class_header += f"from {baseclass} import {baseclass}\n"
                add_linebreaks = True

            for interface in interfaces:
                class_header += f"from {interface} import {interface}\n"
                add_linebreaks = True

            for reference in references:
                class_header += f"from {reference} import {reference}\n"
                add_linebreaks = True

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

        if add_linebreaks:
            class_header += "\n\n"

        class_header += f"class {class_name}{class_ancestors}:\n"

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

        return ""

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
        property_prefix = ""
        met_property = False

        if not is_enum:
            properties_string = "\tdef __init__(self):\n"
            if self._options['encapsulate_all_props']:
                property_prefix = "_"

        for property_def in properties.values():
            if is_enum:
                p = f"\t{property_def['name']}"
                if property_def['default_value']:
                    p += f" = {property_def['default_value']}"
                else:
                    p += " = auto()"
            else:
                p = f"\t\tself.{property_prefix}{property_def['name']}"
                if property_def['default_value']:
                    p += f" = {property_def['default_value']}"
                else:
                    p += f" = {self._default_value(property_def['type'])}"

            p += "\n"

            properties_string += p
            met_property = True

        if not met_property:
            properties_string += "\t\tpass\n"

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
                property_name = property_def['name']
                if self._options['encapsulate_all_props']:
                    property_name = f"_{property_name}"

                accessor_name = self._accessor_name(property_name)
                parameter_name = self._parameter_name(property_name)

                accessors_string += (f"\t@property\n\tdef {accessor_name}(self):\n"
                                     f"\t\treturn self.{property_name}\n\n")

                accessors_string += (f"\t@{accessor_name}.setter\n"
                                     f"\tdef {accessor_name}(self, {parameter_name}):\n"
                                     f"\t\tself.{property_name} = {parameter_name}\n\n")

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
            m = ""
            if class_type in ("interface", "abstract class"):
                m += "\t@abstractmethod\n"
            m += f"\tdef {method_def['name']}(self):\n\t\tpass\n\n"
            methods_string += m

        # inherited abstract methods
        if class_type in ("class", "abstract class"):
            comment = "# Todo: implementation this method!"
            for interface_method in interface_methods:
                m = f"\tdef {interface_method['name']}(self):\n\t\t{comment}\n\t\tpass\n\n"
                methods_string += m

        return methods_string

    def _generate_default_ctor(self, class_name):
        return ""

    def _generate_full_arg_ctor(self, class_name, properties):
        return ""

    def _generate_equal_hashcode(self, class_name, properties):
        prefix = ""
        if self._options['encapsulate_all_props']:
            prefix = "_"

        method_string = "\tdef __members(self):\n"
        method_string += "\t\treturn ("
        method_string += ', '.join([f"self.{prefix}{p['name']}" for p in properties.values()])
        method_string += ")\n\n"

        method_string += "\tdef __eq__(self, other):\n"
        method_string += "\t\tif type(other) is type(self):\n"
        method_string += "\t\t\treturn self.__members() == other.__members()\n"
        method_string += "\t\treturn False\n\n"

        method_string += "\tdef __hash__(self):\n"
        method_string += "\t\treturn hash(self.__members())\n\n"

        return method_string

    def _generate_to_string(self, class_name, properties):
        prefix = ""
        if self._options['encapsulate_all_props']:
            prefix = "_"

        method_string = "\tdef __str__(self):\n"
        method_string += f"\t\treturn f\"{class_name} [{{"
        method_string += ', '.join([f"'{p['name']}': self.{prefix}{p['name']}" for p in properties.values()])
        method_string += "}]\"\n\n"

        return method_string

    def _package_directive(self, package_name):
        return None

    def _map_type(self, typename):
        return None

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
        param_list = "("

        for _ndx in range(len(param_types)):
            if _ndx > 0:
                param_list += ", "
            param_list += f"arg{_ndx}"

        param_list += ")"

        return param_list

    def _get_file_extension(self):
        return "py"
