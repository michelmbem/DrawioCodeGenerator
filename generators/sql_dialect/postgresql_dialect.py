from generators.sql_dialect.sql_dialect import SQLDialect


class PostgreSQLDialect(SQLDialect):

    TYPE_MAPPINGS = {
        "boolean": "boolean",
        "bool": "boolean",
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
        "double": "double precision",
        "bigint": "decimal(30, 0)",
        "decimal": "numeric(30, 10)",
        "string": "character varying(255)",
        "wstring": "character varying(255)",
        "date": "date",
        "time": "time",
        "datetime": "datetime",
        "timestamp": "timestamp",
        "unspecified": "int",
    }

    SERIAL_TYPE_MAPPINGS = {
        "short": "smallserial",
        "int16": "smallserial",
        "ushort": "smallserial",
        "uint16": "smallserial",
        "integer": "serial",
        "int": "serial",
        "int32": "serial",
        "uint": "serial",
        "uint32": "serial",
        "long": "bigserial",
        "int64": "bigserial",
        "ulong": "bigserial",
        "uint64": "bigserial",
        "unspecified": "bigserial",
    }

    def map_type(self, typename, constraints):
        if constraints.get("identity", False):
            return self.SERIAL_TYPE_MAPPINGS.get(typename.lower(), "serial")
        return self.TYPE_MAPPINGS.get(typename.lower(), typename)

    def identity_spec(self):
        return ""
