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
        "bigint": "decimal(30)",
        "decimal": "numeric(30, 10)",
        "string": "character varying(255)",
        "wstring": "character varying(255)",
        "date": "date",
        "time": "time",
        "datetime": "datetime",
        "timestamp": "timestamp",
        "uuid": "uuid",
        "guid": "uuid",
        "byte[]": "bytea",
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

    LOB_TYPE_MAPPINGS = {
        "string": "text",
        "wstring": "text",
    }

    def __init__(self):
        super().__init__(True)

    def catalog_switch_directive(self, catalog_name):
        return f"\\c {catalog_name};\n\n"

    def map_type(self, typename, constraints):
        lower_typename = typename.lower()

        if constraints:
            if constraints.get("identity"):
                return self.SERIAL_TYPE_MAPPINGS.get(lower_typename, "serial")

            if constraints.get("lob"):
                lob_type = self.LOB_TYPE_MAPPINGS.get(lower_typename)
                if lob_type: return lob_type

        return self.TYPE_MAPPINGS.get(lower_typename, typename)

    def identity_spec(self):
        return ""

    def enum_decl(self, class_def):
        enum_members = ", ".join(f"'{m['name']}'" for m in class_def['properties'].values())
        return f"create type {class_def['name']} enum({enum_members});\n\n"

    def enum_spec(self, type_name, type_members):
        return type_name
