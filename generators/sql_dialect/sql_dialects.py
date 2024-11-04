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
        match dialect.lower(): 
            case "ansi":
                return AnsiSQLDialect()
            case "mysql":
                return MySQLDialect()
            case "postgresql":
                return PostgreSQLDialect()
            case "firebird":
                return FirebirdDialect()
            case "oracle":
                return OracleDialect()
            case "db2":
                return DB2Dialect()
            case "sqlserver":
                return SQLServerDialect()
            case "sybase":
                return SybaseDialect()
            case "access":
                return AccessDialect()
            case "sqlite":
                return SQLiteDialect()
            case "derby":
                return DerbyDialect()
            case "hsqldb":
                return HSQLDBDialect()
            case "h2":
                return H2Dialect()
            case _:
                raise ValueError(f"Could not find an implementation of SQLDialect for the '{dialect}' dialect")
