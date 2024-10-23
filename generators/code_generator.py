import re
import traceback

from os import makedirs, path
from abc import ABC, abstractmethod


class CodeGenerator(ABC):
    """
    Base class of all code generators

    Parameters:
        syntax_tree: syntax tree of the drawio file
        file_path: path for the code files to be written to
        options: set of additional options
    """

    def __init__(self, syntax_tree, file_path, options):
        self._syntax_tree = syntax_tree
        self._file_path = path.abspath(file_path)
        self._options = options
        self._files = []

    @staticmethod
    def _ensure_dir_exists(dir_path):
        makedirs(dir_path, exist_ok=True)

    @staticmethod
    def _split_package_name(package_name):
        return re.split(r"[./\\]|::", package_name)

    def generate_code(self):
        """
        Use the syntax tree to generate code files for the UML class diagrams
        """

        print("<<< GENERATING CODE FILES FROM SYNTAX TREE >>>")

        try:
            self._ensure_dir_exists(self._file_path)

            for class_def in self._syntax_tree.values():
                baseclasses, interfaces, references = self._get_class_dependencies(class_def)

                file_contents = self._generate_class_header(class_def['type'], class_def['name'], baseclasses, interfaces, references)
                file_contents += self._generate_properties(class_def['properties'], class_def['type'] == "enum")
                file_contents += "\n"

                if class_def['type'] in ("class", "abstract class"):
                    file_contents += self._generate_property_accessors(class_def['properties'])

                if class_def['type'] != "enum":
                    interface_methods = []
                    self._get_interface_methods(class_def['relationships']['implements'], interface_methods)
                    file_contents += self._generate_methods(class_def['methods'], class_def['type'], interface_methods)

                file_contents += self._generate_class_footer(class_def['type'], class_def['name'])

                self._files.append((class_def['name'], file_contents))

            self._generate_files()
        except Exception as e:
            print(f"{self.__class__.__name__}.generate_code ERROR: {e}")
            traceback.print_exception(e)

    def _generate_files(self):
        """
        Write generated code to file

        Returns:
            boolean: True if successful, False if unsuccessful
        """

        print(f"<<< WRITING FILES TO {self._file_path} >>>")

        try:
            for filename, contents in self._files:
                file_path = path.join(self._file_path, f"{filename}.{self._get_file_extension()}")
                with open(file_path, "w") as f:
                    f.write(contents)
        except Exception as e:
            print(f"{self.__class__.__name__}.generate_files ERROR: {e}")
            traceback.print_exception(e)

    def _get_class_dependencies(self, class_def):
        """
        Get a tuple of all the classes that this class depends on

        :param class_def: the current class
        :return: a tuple of baseclasses, implemented interfaces and referenced classes
        """

        baseclasses = []
        if len(class_def['relationships']['extends']) > 0:
            baseclasses += [self._syntax_tree[r]['name'] for r in class_def['relationships']['extends']]

        interfaces = []
        if len(class_def['relationships']['implements']) > 0:
            interfaces += [self._syntax_tree[r]['name'] for r in class_def['relationships']['implements']]

        references = []
        if len(class_def['relationships']['association']) > 0:
            references += [self._syntax_tree[r]['name'] for r in class_def['relationships']['association']]
        if len(class_def['relationships']['aggregation']) > 0:
            references += [self._syntax_tree[r]['name'] for r in class_def['relationships']['aggregation']]
        if len(class_def['relationships']['composition']) > 0:
            references += [self._syntax_tree[r]['name'] for r in class_def['relationships']['composition']]

        return baseclasses, interfaces, references

    def _get_interface_methods(self, interface_ids, interface_methods):
        """
        Get the interface methods that require implementation

        Parameters:
            interface_ids: list of interface ids
            interface_methods: list of interface methods
        """

        for interface_id in interface_ids:
            interface = self._syntax_tree[interface_id]
            interface_methods += interface['methods'].values()
            self._get_interface_methods(interface['relationships']['implements'], interface_methods)

    @abstractmethod
    def _generate_class_header(self, class_type, class_name, baseclasses, interfaces, references):
        pass

    @abstractmethod
    def _generate_class_footer(self, class_type, class_name):
        pass
    
    @abstractmethod
    def _generate_properties(self, properties, is_enum):
        pass

    @abstractmethod
    def _generate_property_accessors(self, properties):
        pass

    @abstractmethod
    def _generate_methods(self, methods, class_type, interface_methods):
        pass

    @abstractmethod
    def _package_directive(self, package_name):
        pass

    @abstractmethod
    def _map_type(self, typename):
        pass

    @abstractmethod
    def _default_value(self, typename):
        pass

    @abstractmethod
    def _get_parameter_list(self, param_types):
        pass

    @abstractmethod
    def _get_file_extension(self):
        pass
