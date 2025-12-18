from connection.db import engine
from sqlalchemy import text
import bcrypt

def login_user(username, password):
    try:
        with engine.connect() as conn:
            query =text(
                "SELECT id, username, password, role FROM users WHERE username = :username LIMIT 1",
            )
            user = conn.execute(query, {"username": username}).fetchone()

            if not user:
                return False, "Хэрэглэгч олдсонгүй", None

            user_id, username_db, hashed_password, role = user

            # password шалгах
            if not bcrypt.checkpw(
                password.encode("utf-8"),
                hashed_password.encode("utf-8") if isinstance(hashed_password, str) else hashed_password
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


