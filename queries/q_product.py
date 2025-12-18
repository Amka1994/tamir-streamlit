from connection.db import engine
from sqlalchemy import text

# Бараа нэмэх функц
def insert_product(name, code, quantity, category, price):
   
    try:
        with engine.begin() as conn:
            query = text(
                "INSERT INTO products (name, code, quantity, category, price) VALUES (:name, :code, :quantity, :category, :price)"
            )

            conn.execute(query, {
                "name": name,
                "code": code,
                "quantity": quantity,
                "category": category,
                "price": price
            })
            return True, "Бараа амжилттай бүртгэгдлээ"
    except Exception as e:
        return False, f"Алдаа гарлаа: {e}"
  
# Бүх барааг авах функц
def get_all_products():
    try:
        with engine.connect() as conn:

             query = text("SELECT id, name, code, quantity, category, price FROM products")
             result = conn.execute(query)
             return result
    except Exception as e:
        print(f"Алдаа гарлаа: {e}")
        return []
    finally:
        conn.close()
