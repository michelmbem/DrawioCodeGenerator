from generators.sql_dialect.sql_dialect import SQLDialect


class DB2Dialect(SQLDialect):

    TYPE_MAPPINGS = {
        "boolean": "smallint",
        "bool": "smallint",
        "char": "character(1)",
        "wchar": "character(1)",
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
        "double": "double",
        "bigint": "decimal(30)",
        "decimal": "decimal(30, 10)",
        "string": "varchar(255)",
        "wstring": "varchar(255)",
        "date": "date",
        "time": "time",
        "datetime": "timestamp",
        "timestamp": "timestamp",
        "uuid": "char(16)",
        "guid": "char(16)",
        "byte[]": "blob",
        "unspecified": "integer",
    }

    LOB_TYPE_MAPPINGS = {
        "string": "clob",
        "wstring": "dclob",
    }

    def __init__(self):
        super().__init__()
