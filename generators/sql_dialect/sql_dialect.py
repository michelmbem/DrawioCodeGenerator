class SQLDialect:
    def map_type(self, typename, constraints):
        return self.TYPE_MAPPINGS.get(typename.lower(), typename)

    def identity_spec(self):
        return "generated always as identity (start with 1, increment by 1)"
