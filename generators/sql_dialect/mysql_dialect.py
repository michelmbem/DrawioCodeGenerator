from generators.sql_dialect.sql_dialect import SQLDialect


class MySQLDialect(SQLDialect):

    TYPE_MAPPINGS = {
        "boolean": "tinyint(1)",
        "bool": "tinyint(1)",
        "char": "char(1)",
        "wchar": "char(1)",
        "sbyte": "tinyint",
        "int8": "tinyint",
        "byte": "tinyint unsigned",
        "uint8": "tinyint unsigned",
        "short": "smallint",
        "int16": "smallint",
        "ushort": "smallint unsigned",
        "uint16": "smallint unsigned",
        "integer": "int",
        "int": "int",
        "int32": "int",
        "uint": "int unsigned",
        "uint32": "int unsigned",
        "long": "bigint",
        "int64": "bigint",
        "ulong": "bigint unsigned",
        "uint64": "bigint unsigned",
        "float": "float(24)",
        "single": "float(24)",
        "double": "float(53)",
        "bigint": "decimal(30, 0)",
        "decimal": "decimal(30, 10)",
        "string": "varchar(255)",
        "wstring": "varchar(255)",
        "date": "date",
        "time": "time",
        "datetime": "datetime",
        "timestamp": "timestamp",
        "unspecified": "int",
    }

    def map_type(self, typename, constraints):
        return self.TYPE_MAPPINGS.get(typename.lower(), typename)

    def identity_spec(self):
        return "auto_increment"
