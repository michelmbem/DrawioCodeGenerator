from generators.sql_dialect.sql_dialect import SQLDialect


class AccessDialect(SQLDialect):

    TYPE_MAPPINGS = {
        "boolean": "bit",
        "bool": "bit",
        "char": "text(1)",
        "wchar": "text(1)",
        "sbyte": "byte",
        "int8": "byte",
        "byte": "byte",
        "uint8": "byte",
        "short": "integer",
        "int16": "integer",
        "ushort": "integer",
        "uint16": "integer",
        "integer": "long",
        "int": "long",
        "int32": "long",
        "uint": "long",
        "uint32": "long",
        "long": "decimal(20)",
        "int64": "decimal(20)",
        "ulong": "decimal(20)",
        "uint64": "decimal(20)",
        "float": "single",
        "single": "single",
        "double": "double",
        "bigint": "decimal(30)",
        "decimal": "decimal(30, 10)",
        "string": "text(255)",
        "wstring": "text(255)",
        "date": "datetime",
        "time": "datetime",
        "datetime": "datetime",
        "timestamp": "datetime",
        "uuid": "uniqueidentifier",
        "guid": "uniqueidentifier",
        "byte[]": "oleobject",
        "unspecified": "long",
    }

    LOB_TYPE_MAPPINGS = {
        "string": "memo",
        "wstring": "memo",
    }

    def __init__(self):
        super().__init__()

    def map_type(self, typename, constraints):
        lower_typename = typename.lower()

        if constraints:
            if constraints.get("identity"):
                return "counter(1, 1)"

            if constraints.get("lob"):
                lob_type = self.LOB_TYPE_MAPPINGS.get(lower_typename)
                if lob_type: return lob_type

        return self.TYPE_MAPPINGS.get(lower_typename, typename)

    def identity_spec(self):
        return ""
