from generators.sql_dialect.sql_dialect import SQLDialect


class SQLiteDialect(SQLDialect):

    TYPE_MAPPINGS = {
        "boolean": "integer",
        "bool": "integer",
        "char": "text",
        "wchar": "text",
        "sbyte": "integer",
        "int8": "integer",
        "byte": "integer",
        "uint8": "integer",
        "short": "integer",
        "int16": "integer",
        "ushort": "integer",
        "uint16": "integer",
        "integer": "integer",
        "int": "integer",
        "int32": "integer",
        "uint": "integer",
        "uint32": "integer",
        "long": "integer",
        "int64": "integer",
        "ulong": "integer",
        "uint64": "integer",
        "float": "real",
        "single": "real",
        "double": "real",
        "bigint": "numeric",
        "decimal": "numeric",
        "string": "text",
        "wstring": "text",
        "date": "text",
        "time": "text",
        "datetime": "text",
        "timestamp": "text",
        "uuid": "text",
        "guid": "text",
        "unspecified": "integer",
    }

    def __init__(self):
        super().__init__()

    def identity_spec(self):
        return ""
