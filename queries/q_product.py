from connection.db import engine
from sqlalchemy import text

# Бараа нэмэх функц
def insert_product(name, code, category, price):
   
    try:
        with engine.begin() as conn:
            query = text(
                "INSERT INTO products (name, code, category, price) VALUES (:name, :code, :category, :price)"
            )

            conn.execute(query, {
                "name": name,
                "code": code,
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


#history-г авах функц
def get_product_history(product_id: int = None, limit: int = 100):
    try:
        with engine.connect() as conn:
            # Бүх барааны түүх
            if product_id is None:
                query = text("""select
                    ph.changed_at,
                    p.name AS product_name,
                    ph.change_type,
                    ph.quantity_change,
                    ph.previous_quantity,
                    ph.new_quantity,
                    ph.reason,
                    ph.changed_by,
                    p.category
                    FROM log_product_history ph
                    join products p on ph.product_id = p.id
                    ORDER BY ph.changed_at DESC
                    LIMIT :limit
                    """)
                result = conn.execute(query, {"limit": limit})
            else:
                # Тухайн барааны түүх
                query = text("""SELECT ph.changed_at, ph.change_type,
                           ph.quantity_change, ph.previous_quantity, ph.new_quantity,
                           ph.reason, ph.changed_by, ph.category
                            FROM log_product_history ph
                            WHERE ph.product_id = :pid
                            ORDER BY ph.changed_at DESC
                            LIMIT :limit
                        """)
                result = conn.execute(query, {"pid": product_id, "limit": limit})
            return result.fetchall()
    except Exception as e:
        print(f"Алдаа гарлаа: {e}")
        return []
         
   