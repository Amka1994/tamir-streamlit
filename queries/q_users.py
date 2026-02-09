import logging
import bcrypt
from sqlalchemy import text

from connection.db import engine

logger = logging.getLogger(__name__)


def add_user_to_db(username: str, password: str) -> tuple[bool, str]:
    try:
        with engine.begin() as conn:
            check_query = text(
                "SELECT id FROM users WHERE username = :username LIMIT 1")
            result = conn.execute(check_query, {"username": username}).fetchone()



            # password hash
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            # hereglegch nemeh
            insert_query = text("""
                INSERT INTO users (username, password)
                VALUES (:username, :hashed_password)
            """)
            conn.execute(insert_query, {
                "username": username,
                "hashed_password": hashed_password
            })

            return True, "Хэрэглэгч амжилттай нэмэгдлээ"

    except Exception as e:
        logger.exception("add_user_to_db алдаа: %s", e)
        return False, str(e)
