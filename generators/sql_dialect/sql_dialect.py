class SQLDialect:

    def __init__(self, multi_catalog = False):
        self._multi_catalog = multi_catalog

    @property
    def multi_catalog(self):
        return self._multi_catalog

    def catalog_switch_directive(self, catalog_name):
        return f"use {catalog_name};\n\n"

    def map_type(self, typename, constraints):
        lower_typename = typename.lower()

        if constraints and constraints.get("lob"):
            lob_type = self.LOB_TYPE_MAPPINGS.get(lower_typename)
            if lob_type: return lob_type

        return self.TYPE_MAPPINGS.get(lower_typename, typename)

    def escape(self, name):
        return f'"{name}"'

    def identity_spec(self):
        return "generated always as identity (start with 1, increment by 1)"

    def enum_decl(self, class_def):
        return ""

    def enum_spec(self, type_name, type_members):
        return self.map_type("string", None)
