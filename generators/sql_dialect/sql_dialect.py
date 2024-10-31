from abc import ABC, abstractmethod


class SQLDialect(ABC):

    @abstractmethod
    def map_type(self, typename, constraints):
        pass

    @abstractmethod
    def identity_spec(self):
        pass

    @abstractmethod
    def fk_name(self, table, foreign_table, index):
        pass
