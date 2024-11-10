from generators.sql_dialect.sql_dialect import SQLDialect


class AnsiSQLDialect(SQLDialect):

    TYPE_MAPPINGS = {
        "boolean": "boolean",
        "bool": "boolean",
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
        "long": "bigint",
        "int64": "bigint",
        "ulong": "bigint",
        "uint64": "bigint",
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
        "uuid": "character(36)",
        "guid": "character(36)",
        "byte[]": "binary large object",
        "unspecified": "integer",
    }

    LOB_TYPE_MAPPINGS = {
        "string": "character large object",
        "wstring": "character large object",
    }

    def __init__(self):
        super().__init__()
