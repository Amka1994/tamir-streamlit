
from connection.db import engine
from sqlalchemy import text


def add_product_quantity(product_id: int, add_quantity: int, reason: str="", changed_by: str="system"):
    if add_quantity <= 0:
        return False, "Нэмэх тоо ширхэг 0-ээс их байх ёстой."
    try:
        with engine.begin() as conn:

            current_query = text("select quantity from products where id = :pid")
            result = conn.execute(current_query, {"pid": product_id}).fetchone()

            if not result:
                return False, "Бараа олдсонгүй."
            
            current_qty = result[0]                    # 
            new_qty = current_qty + add_quantity
            
            #Тоог шинэчлэх
            update_query = text("UPDATE products SET quantity = :new_qty WHERE id = :pid")
            conn.execute(update_query, {"new_qty": new_qty, "pid": product_id})


            #log бичих
            history_query = text("""
                INSERT INTO log_product_history 
                (product_id, change_type, quantity_change, previous_quantity, new_quantity, reason, changed_by) 
                VALUES 
                (:product_id, :change_type, :quantity_change, :previous_quantity, :new_quantity, :reason, :changed_by)
            """)

            conn.execute(history_query, {
                "product_id": product_id,
                "change_type": "ADD",
                "quantity_change": add_quantity,
                "previous_quantity": current_qty,
                "new_quantity": new_qty,
                "reason": reason or "Тоо нэмсэн",
                "changed_by": changed_by
            })
        return True, f"Амжилттай +{add_quantity} нэмэгдлээ. Шинэ тоо: {new_qty}"
    except Exception as e:
        return False, f"Алдаа гарлаа: {e}"
