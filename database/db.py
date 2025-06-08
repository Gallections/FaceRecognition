import psycopg2
from database.queries import *
import json
import numpy as np

def get_connection():
    conn = psycopg2.connect(
        database="facialRecognition",
        user="postgres",  # tells postgres which database inside your local Postgres server to use.
        password="bili23",
        host="localhost",  # tells postgres where to find the databases.
        port="5432"  # tell the port for the postgres
    )
    conn.autocommit = True
    return conn

def close_connection(conn):
    conn.close()

def run_schema(conn, schema_file_path):
    cursor = conn.cursor()
    try:
        with open(schema_file_path, 'r') as f:
            sql = f.read()
            cursor.execute(sql)
    except Exception as e:
        print("Failed to execute the schema sql file, ", e)
    finally:
        cursor.close()
        # conn.close()


sampleFloat64 = np.random.rand(128).astype(np.float64)
jsonSample = json.dumps(sampleFloat64.tolist())

if __name__ == "__main__":
    conn = get_connection()
    # run_schema(conn, "schema.sql")
    # insert_name(conn, 'Brennan', 'Johnson')
    # insert_face_encoding(conn, 'f20662bc-6969-4458-9a7c-57175afb239b', jsonSample)
    remove_name(conn, 'f20662bc-6969-4458-9a7c-57175afb239b')
    close_connection(conn)



# cursor = conn.cursor()
# cursor.execute("select * from employee")
# data = cursor.fetchall()
#
# for d in data:
#     print(d)
# conn.close()