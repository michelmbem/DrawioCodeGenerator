from generators.sql_dialect.sql_dialect import SQLDialect


class SybaseDialect(SQLDialect):

    TYPE_MAPPINGS = {
        "boolean": "bit",
        "bool": "bit",
        "char": "char(1)",
        "wchar": "unichar(1)",
        "sbyte": "tinyint",
        "int8": "tinyint",
        "byte": "unsigned tinyint",
        "uint8": "unsigned tinyint",
        "short": "smallint",
        "int16": "smallint",
        "ushort": "unsigned smallint",
        "uint16": "unsigned smallint",
        "integer": "int",
        "int": "int",
        "int32": "int",
        "uint": "unsigned int",
        "uint32": "unsigned int",
        "long": "bigint",
        "int64": "bigint",
        "ulong": "unsigned bigint",
        "uint64": "unsigned bigint",
        "float": "real",
        "single": "real",
        "double": "float",
        "bigint": "decimal(30)",
        "decimal": "decimal(30, 10)",
        "string": "varchar(255)",
        "wstring": "univarchar(255)",
        "date": "date",
        "time": "time",
        "datetime": "datetime",
        "timestamp": "datetime",
        "unspecified": "int",
    }

    def __init__(self):
        super().__init__(True)

    def identity_spec(self):
        return "identity(1, 1)"
