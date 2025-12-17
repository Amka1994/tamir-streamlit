from connection.db import get_db_connection
import bcrypt

def login_user(username, password):
    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            # хэрэглэгчийг username-ээр хайх
            cur.execute(
                "SELECT id, username, password, role FROM users WHERE username=%s",
                (username,)
            )
            user = cur.fetchone()

            if not user:
                return False, "Хэрэглэгч олдсонгүй", None

            user_id, username_db, hashed_password, role = user

            # password шалгах
            if not bcrypt.checkpw(
                password.encode("utf-8"),
                hashed_password.encode("utf-8")
            ):
                return False, "Нууц үг буруу байна", None

            # амжилттай login
            return True, "Амжилттай нэвтэрлээ", {
                "id": user_id,
                "username": username_db,
                "role": role
            }

    except Exception as e:
        return False, f"Алдаа гарлаа: {e}", None

    finally:
        conn.close()
