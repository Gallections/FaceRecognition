from database import get_connection

def insert_name(conn, first_name, last_name, full_name=""):
    if not full_name:
        full_name = f"{first_name} {last_name}"
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO name (first_name, last_name, full_name) VALUES (%s, %s, %s)",
                (first_name, last_name, full_name)
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

def remove_name(conn, id):
    try:
        with conn.cursor() as cursor:  # using context manager automatically closes the cursor when done
            cursor.execute("DELETE FROM name WHERE id = %s", (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
