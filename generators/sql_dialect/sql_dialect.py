from abc import ABC, abstractmethod


class SQLDialect(ABC):

    @abstractmethod
    def map_type(self, typename, constraints):
        pass

    @abstractmethod
    def identity_spec(self):
        pass
