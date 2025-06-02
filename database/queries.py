def insert_name(conn, first_name, last_name, full_name=""):
    if not full_name:
        full_name = f"{first_name} {last_name}"
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO name (first_name, last_name, full_name) VALUES (%s, %s, %s)"
                "RETURNING id",
                (first_name, last_name, full_name)
            )
            new_id = cursor.fetchone()[0]
        conn.commit()
        print(new_id)
        return new_id
    except Exception as e:
        conn.rollback()
        print(e)
        raise e

def remove_name(conn, id):
    try:
        with conn.cursor() as cursor:  # using context manager automatically closes the cursor when done
            cursor.execute("DELETE FROM name WHERE id = %s", (id,))
        conn.commit()
        print(f"Successfully removed {id} from name.")
    except Exception as e:
        conn.rollback()
        raise e

# The encoding is expected to be a JSON format
def insert_face_encoding(conn, person_id, encoding):
    try:
        query = ("INSERT INTO encoding (person_id, face_encoding)"
                 "VALUES (%s, %s)"
                 "RETURNING id")

        with conn.cursor() as cursor:
            cursor.execute(query, (person_id, encoding))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

def remove_face_encoding(conn, id):
    try:
        with conn.cursor() as cursor:  # using context manager automatically closes the cursor when done
            cursor.execute("DELETE FROM name WHERE id = %s", (id,))
        conn.commit()
        print(f"Successfully removed {id} from encoding.")
    except Exception as e:
        conn.rollback()
        raise e