import psycopg2

def get_connection():
    conn = psycopg2.connect(
        database="facialRecognition",
        user="postgres",  # tells postgres which database inside your local Postgres server to use.
        password="bili23",
        host="localhost",  # tells postgres where to find the databases.
        port="5432"  # tell the port for the postgres
    )
    return conn

# cursor = conn.cursor()
# cursor.execute("select * from employee")
# data = cursor.fetchall()
#
# for d in data:
#     print(d)
# conn.close()