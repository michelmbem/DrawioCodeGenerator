from os import path, makedirs
from abc import ABC, abstractmethod


class CodeGeneratorInterface(ABC):
    """
    Interface contract for code generation
    """

    @staticmethod
    def ensure_dir_exists(dir_path):
        if not path.isdir(dir_path):
            makedirs(dir_path)

    @abstractmethod
    def generate_code(self):
        pass

    @abstractmethod
    def generate_classes(self, class_type, class_name, extends, implements):
        pass

    @abstractmethod
    def get_classes(self):
        pass
    
    @abstractmethod
    def generate_properties(self, properties):
        pass
    
    @abstractmethod
    def get_properties(self):
        pass

    @abstractmethod
    def generate_property_accessors(self, properties):
        pass

    @abstractmethod
    def get_property_accessors(self):
        pass

    @abstractmethod
    def generate_methods(self, methods, properties, class_type, interface_methods):
        pass

    @abstractmethod
    def get_methods(self):
        pass

    @abstractmethod
    def generate_files(self):
        pass
    
    @abstractmethod
    def get_files(self):
        pass
