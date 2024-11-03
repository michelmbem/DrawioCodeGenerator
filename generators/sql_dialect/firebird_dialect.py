from generators.sql_dialect.sql_dialect import SQLDialect


class FirebirdDialect(SQLDialect):

    TYPE_MAPPINGS = {
        "boolean": "boolean",
        "bool": "boolean",
        "char": "char(1)",
        "wchar": "nchar(1)",
        "sbyte": "smallint",
        "int8": "smallint",
        "byte": "smallint",
        "uint8": "smallint",
        "short": "smallint",
        "int16": "smallint",
        "ushort": "smallint",
        "uint16": "smallint",
        "integer": "integer",
        "int": "integer",
        "int32": "integer",
        "uint": "integer",
        "uint32": "integer",
        "long": "bigint",
        "int64": "bigint",
        "ulong": "bigint",
        "uint64": "bigint",
        "float": "float",
        "single": "float",
        "double": "double precision",
        "bigint": "decimal(30)",
        "decimal": "decimal(30, 10)",
        "string": "varchar(255)",
        "wstring": "nvarchar(255)",
        "date": "date",
        "time": "time",
        "datetime": "timestamp",
        "timestamp": "timestamp",
        "unspecified": "integer",
    }

    def __init__(self):
        super().__init__()

    def identity_spec(self):
        return ""