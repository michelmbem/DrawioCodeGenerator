from generators.sql_dialect.sql_dialect import SQLDialect


class HSQLDBDialect(SQLDialect):

    TYPE_MAPPINGS = {
        "boolean": "boolean",
        "bool": "boolean",
        "char": "char(1)",
        "wchar": "char(1)",
        "sbyte": "tinyint",
        "int8": "tinyint",
        "byte": "tinyint",
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
        "double": "float",
        "bigint": "decimal(30)",
        "decimal": "decimal(30, 10)",
        "string": "varchar(255)",
        "wstring": "varchar(255)",
        "date": "date",
        "time": "time",
        "datetime": "timestamp",
        "timestamp": "timestamp",
        "uuid": "uuid",
        "guid": "uuid",
        "unspecified": "integer",
    }

    def __init__(self):
        super().__init__()
