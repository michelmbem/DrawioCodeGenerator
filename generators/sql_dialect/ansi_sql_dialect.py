from generators.sql_dialect.sql_dialect import SQLDialect


class AnsiSQLDialect(SQLDialect):

    TYPE_MAPPINGS = {
        "boolean": "smallint",
        "bool": "smallint",
        "char": "character(1)",
        "wchar": "national character(1)",
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
        "long": "decimal(20)",
        "int64": "decimal(20)",
        "ulong": "decimal(20)",
        "uint64": "decimal(20)",
        "float": "real",
        "single": "real",
        "double": "double precision",
        "bigint": "decimal(30)",
        "decimal": "decimal(30, 10)",
        "string": "character varying(255)",
        "wstring": "national character varying(255)",
        "date": "date",
        "time": "time",
        "datetime": "timestamp",
        "timestamp": "timestamp",
        "unspecified": "integer",
    }

    def __init__(self):
        super().__init__()
