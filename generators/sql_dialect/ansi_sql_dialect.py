from generators.sql_dialect.sql_dialect import SQLDialect


class AnsiSQLDialect(SQLDialect):

    TYPE_MAPPINGS = {
        "boolean": "boolean",
        "bool": "boolean",
        "char": "character(1)",
        "wchar": "national character(1)",
        "sbyte": "tinyint",
        "int8": "tinyint",
        "byte": "tinyint",
        "uint8": "tinyint",
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
        "bigint": "decimal(30, 0)",
        "decimal": "numeric(30, 10)",
        "string": "character varying(255)",
        "wstring": "national character varying(255)",
        "date": "date",
        "time": "time",
        "datetime": "datetime",
        "timestamp": "timestamp",
        "unspecified": "integer",
    }

    def map_type(self, typename, constraints):
        return self.TYPE_MAPPINGS.get(typename.lower(), typename)

    def identity_spec(self):
        return "autoincrement"

    def fk_name(self, table, foreign_table, index):
        return f"fk_{table}_{foreign_table}"
