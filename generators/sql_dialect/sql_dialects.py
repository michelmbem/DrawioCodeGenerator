from generators.sql_dialect.ansi_sql_dialect import AnsiSQLDialect
from generators.sql_dialect.mysql_dialect import MySQLDialect
from generators.sql_dialect.postgresql_dialect import PostgreSQLDialect
from generators.sql_dialect.firebird_dialect import FirebirdDialect
from generators.sql_dialect.oracle_dialect import OracleDialect
from generators.sql_dialect.db2_dialect import DB2Dialect
from generators.sql_dialect.sqlserver_dialect import SQLServerDialect
from generators.sql_dialect.sybase_dialect import SybaseDialect
from generators.sql_dialect.access_dialect import AccessDialect
from generators.sql_dialect.sqlite_dialect import SQLiteDialect
from generators.sql_dialect.derby_dialect import DerbyDialect
from generators.sql_dialect.hsqldb_dialect import HSQLDBDialect
from generators.sql_dialect.h2_dialect import H2Dialect


class SQLDialects:

    @staticmethod
    def get(dialect):
        dialect = dialect.lower()
        if dialect == "ansi":
            return AnsiSQLDialect()
        elif dialect == "mysql":
            return MySQLDialect()
        elif dialect == "postgresql":
            return PostgreSQLDialect()
        elif dialect == "firebird":
            return FirebirdDialect()
        elif dialect == "oracle":
            return OracleDialect()
        elif dialect == "db2":
            return DB2Dialect()
        elif dialect == "sqlserver":
            return SQLServerDialect()
        elif dialect == "sybase":
            return SybaseDialect()
        elif dialect == "access":
            return AccessDialect()
        elif dialect == "sqlite":
            return SQLiteDialect()
        elif dialect == "derby":
            return DerbyDialect()
        elif dialect == "hsqldb":
            return HSQLDBDialect()
        elif dialect == "h2":
            return H2Dialect()
        else:
            raise ValueError(f"Could not find an implementation of SQLDialect for the '{dialect}' dialect")
