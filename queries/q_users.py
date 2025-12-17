from connection.db import get_db_connection
import bcrypt

def add_user_to_db(username, password):
    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            # username давхардал шалгах
            cur.execute(
                "SELECT id FROM users WHERE username=%s",
                (username,)
            )
            if cur.fetchone():
                return False, "Хэрэглэгчийн нэр аль хэдийн байна"

            # password hash
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            # insert
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, hashed_password)
            )
            conn.commit()

            return True, "Хэрэглэгч амжилттай нэмэгдлээ"

    except Exception as e:
        return False, str(e)

    finally:
        conn.close()
