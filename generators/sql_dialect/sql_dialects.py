from generators.sql_dialect.ansi_sql_dialect import AnsiSQLDialect
from generators.sql_dialect.mysql_dialect import MySQLDialect
from generators.sql_dialect.sql_server_dialect import SQLServerDialect
from generators.sql_dialect.postgresql_dialect import PostgreSQLDialect
from generators.sql_dialect.oracle_dialect import OracleDialect


class SQLDialects:

    @staticmethod
    def get(dialect):
        dialect = dialect.lower()
        if dialect == "ansi":
            return AnsiSQLDialect()
        elif dialect == "mysql":
            return MySQLDialect()
        elif dialect == "sqlserver":
            return SQLServerDialect()
        elif dialect == "postgresql":
            return PostgreSQLDialect()
        elif dialect == "oracle":
            return OracleDialect()
        else:
            raise ValueError(f"Could not find an implementation of SQLDialect for the '{dialect}' dialect")
