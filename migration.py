def create_name_table(cursor):
    cursor.execute("create table if not exists name ("
                   "id SERIAL PRIMARY KEY,"
                   "first_name VARCHAR(50) NOT NULL,"
                   "last_name VARCHAR(50) NOT NULL"
                   "full_name VARCHAR(100)"
                   ")")

def print_recent(cursor):
    data = cursor.fetchall()
    for d in data:
        print(d)


def run_migrations(conn):
    # opening connection
    cursor = conn.cursor()

    # migration body
    create_name_table(cursor)


    # closing connection
    conn.commit()
    conn.close()