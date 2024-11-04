from generators.sql_dialect.sql_dialect import SQLDialect


class AccessDialect(SQLDialect):

    TYPE_MAPPINGS = {
        "boolean": "bit",
        "bool": "bit",
        "char": "char",
        "wchar": "char",
        "sbyte": "byte",
        "int8": "byte",
        "byte": "byte",
        "uint8": "byte",
        "short": "smallint",
        "int16": "smallint",
        "ushort": "smallint",
        "uint16": "smallint",
        "integer": "integer",
        "int": "integer",
        "int32": "integer",
        "uint": "integer",
        "uint32": "integer",
        "long": "decimal(20)",
        "int64": "decimal(20)",
        "ulong": "decimal(20)",
        "uint64": "decimal(20)",
        "float": "real",
        "single": "real",
        "double": "float",
        "bigint": "decimal(30)",
        "decimal": "decimal(30, 10)",
        "string": "varchar",
        "wstring": "varchar",
        "date": "datetime",
        "time": "datetime",
        "datetime": "datetime",
        "timestamp": "datetime",
        "uuid": "guid",
        "guid": "guid",
        "unspecified": "integer",
    }

    def __init__(self):
        super().__init__()

    def map_type(self, typename, constraints):
        if constraints.get("identity", False):
            return "counter"
        return self.TYPE_MAPPINGS.get(typename.lower(), typename)

    def identity_spec(self):
        return ""
