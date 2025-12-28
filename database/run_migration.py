"""
Database migration script
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_connection, close_connection, run_schema


def run_migrations():
    """Run database migrations"""
    print("Starting database migration...")
    
    try:
        conn = get_connection()
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        
        print(f"Executing schema from: {schema_path}")
        run_schema(conn, schema_path)
        
        close_connection(conn)
        print("✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_migrations()
