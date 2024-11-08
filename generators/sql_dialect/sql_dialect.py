class SQLDialect:

    def __init__(self, multi_catalog = False):
        self._multi_catalog = multi_catalog

    @property
    def multi_catalog(self):
        return self._multi_catalog

    def map_type(self, typename, constraints):
        return self.TYPE_MAPPINGS.get(typename.lower(), typename)

    def identity_spec(self):
        return "generated always as identity (start with 1, increment by 1)"

    def enum_decl(self, class_def):
        return ""

    def enum_spec(self, type_name, type_members):
        return self.map_type("string", None)
