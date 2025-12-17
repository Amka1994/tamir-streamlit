from connection.db import get_db_connection
from sqlalchemy import text


def insert_product(name, code, quantity, category, price):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO products (name, code, quantity, category, price) VALUES (%s, %s, %s, %s, %s)",
                (name, code, quantity, category, price)
            )
            conn.commit()
            return True, "Бараа амжилттай бүртгэгдлээ"
    except Exception as e:
        return False, f"Алдаа гарлаа: {e}"
    finally:
        conn.close()

def get_all_products():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT name, code, quantity, category, price FROM products")
            products = cur.fetchall()
            return products
    except Exception as e:
        print(f"Алдаа гарлаа: {e}")
        return []
    finally:
        conn.close()