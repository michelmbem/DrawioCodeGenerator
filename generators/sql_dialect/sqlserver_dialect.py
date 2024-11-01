from generators.sql_dialect.sql_dialect import SQLDialect


class SQLServerDialect(SQLDialect):

    TYPE_MAPPINGS = {
        "boolean": "bit",
        "bool": "bit",
        "char": "char(1)",
        "wchar": "nchar(1)",
        "sbyte": "tinyint",
        "int8": "tinyint",
        "byte": "tinyint",
        "uint8": "tinyint",
        "short": "smallint",
        "int16": "smallint",
        "ushort": "smallint",
        "uint16": "smallint",
        "integer": "int",
        "int": "int",
        "int32": "int",
        "uint": "int",
        "uint32": "int",
        "long": "bigint",
        "int64": "bigint",
        "ulong": "bigint",
        "uint64": "bigint",
        "float": "real",
        "single": "real",
        "double": "float",
        "bigint": "decimal(30)",
        "decimal": "decimal(30, 10)",
        "string": "varchar(255)",
        "wstring": "nvarchar(255)",
        "date": "date",
        "time": "time",
        "datetime": "datetime",
        "timestamp": "datetime",
        "unspecified": "int",
    }

    def identity_spec(self):
        return "identity(1, 1)"
