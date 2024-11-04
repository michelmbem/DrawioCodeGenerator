from generators.sql_dialect.sql_dialect import SQLDialect


class OracleDialect(SQLDialect):

    TYPE_MAPPINGS = {
        "boolean": "number(1)",
        "bool": "number(1)",
        "char": "char(1)",
        "wchar": "nchar(1)",
        "sbyte": "number(3)",
        "int8": "number(3)",
        "byte": "number(3)",
        "uint8": "number(3)",
        "short": "number(5)",
        "int16": "number(5)",
        "ushort": "number(5)",
        "uint16": "number(5)",
        "integer": "number(10)",
        "int": "number(10)",
        "int32": "number(10)",
        "uint": "number(10)",
        "uint32": "number(10)",
        "long": "number(20)",
        "int64": "number(20)",
        "ulong": "number(20)",
        "uint64": "number(20)",
        "float": "float(24)",
        "single": "float(24)",
        "double": "float(53)",
        "bigint": "number(30, 0)",
        "decimal": "number(30, 10)",
        "string": "varchar2(255)",
        "wstring": "nvarchar2(255)",
        "date": "date",
        "time": "date",
        "datetime": "date",
        "timestamp": "date",
        "uuid": "raw(16)",
        "guid": "raw(16)",
        "unspecified": "number",
    }

    def __init__(self):
        super().__init__()
