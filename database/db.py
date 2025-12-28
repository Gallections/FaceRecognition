"""
Database connection manager (psycopg v3)
"""
from contextlib import contextmanager
import sys
import os
import psycopg
from psycopg_pool import ConnectionPool

# Add backend to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from config.settings import settings


class DatabaseManager:
    """Manages database connection pool using psycopg v3"""

    _pool: ConnectionPool | None = None

    @classmethod
    def _dsn(cls) -> str:
        return (
            f"dbname={settings.DB_NAME} "
            f"user={settings.DB_USER} "
            f"password={settings.DB_PASSWORD} "
            f"host={settings.DB_HOST} "
            f"port={settings.DB_PORT}"
        )

    @classmethod
    def initialize_pool(cls, minconn: int = 1, maxconn: int = 10):
        """Initialize the connection pool"""
        if cls._pool is None:
            cls._pool = ConnectionPool(conninfo=cls._dsn(), min_size=minconn, max_size=maxconn)

    @classmethod
    def get_connection(cls):
        """Get a connection from the pool"""
        if cls._pool is None:
            cls.initialize_pool()
        # psycopg_pool returns a connection via getconn()
        return cls._pool.getconn()

    @classmethod
    def return_connection(cls, conn):
        """Return a connection to the pool"""
        if cls._pool is not None and conn is not None:
            cls._pool.putconn(conn)

    @classmethod
    def close_all_connections(cls):
        """Close all connections in the pool"""
        if cls._pool is not None:
            cls._pool.close()
            cls._pool = None


@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = DatabaseManager.get_connection()
    try:
        yield conn
    finally:
        DatabaseManager.return_connection(conn)


# Legacy function for backward compatibility
def get_connection():
    """Get a database connection (legacy method)"""
    conn = psycopg.connect(DatabaseManager._dsn())
    conn.autocommit = True
    return conn

def close_connection(conn):
    """Close a database connection"""
    conn.close()


def run_schema(conn, schema_file_path):
    """Execute SQL schema file"""
    cursor = conn.cursor()
    try:
        with open(schema_file_path, 'r') as f:
            sql = f.read()
            cursor.execute(sql)
        conn.commit()
        print("Schema executed successfully")
    except Exception as e:
        print(f"Failed to execute the schema sql file: {e}")
        conn.rollback()
    finally:
        cursor.close()


if __name__ == "__main__":
    # Test database connection
    try:
        conn = get_connection()
        print("Database connection successful!")
        print(f"Connected to: {settings.DB_NAME}")
        close_connection(conn)
    except Exception as e:
        print(f"Database connection failed: {e}")