"""
API dependencies
"""
from database.db import get_db_connection as _get_db_connection, DatabaseManager


def get_db_connection():
    """
    Dependency for getting database connection in FastAPI routes
    """
    conn = DatabaseManager.get_connection()
    try:
        yield conn
    finally:
        DatabaseManager.return_connection(conn)
