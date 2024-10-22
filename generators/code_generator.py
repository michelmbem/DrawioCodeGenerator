from os import makedirs
from abc import ABC, abstractmethod


class CodeGeneratorInterface(ABC):
    """
    Interface contract for code generation
    """

    @staticmethod
    def ensure_dir_exists(dir_path):
        makedirs(dir_path, exist_ok=True)

    @abstractmethod
    def generate_code(self):
        pass

    @abstractmethod
    def generate_class_header(self, class_type, class_name, extends, implements):
        pass
    
    @abstractmethod
    def generate_properties(self, properties, is_enum):
        pass

    @abstractmethod
    def generate_property_accessors(self, properties):
        pass

    @abstractmethod
    def generate_methods(self, methods, class_type, interface_methods):
        pass

    @abstractmethod
    def generate_files(self):
        pass
