from sqlalchemy import text



def save_order_complete(engine, customer_data, card_itmes, total_amount):

    """
    engine: sqlalchemy engine object
    customer_data: dict {'name': '...', 'phone': '...', 'address': '...'}
    card_itmes: list of tuples [{'product_id': 1, quantity': 2, price': 10000}, ...]
    total_amount: float Нийт дүн
    """
    try:
        # engine.begin() нь транзакцыг автоматаар эхлүүлж, 
        # блок дотор алдаа гарвал ROLLBACK, амжилттай бол COMMIT хийнэ.
        with engine.begin() as conn:
            # 1. Хэрэглэгчийг шалгах эсвэл үүсгэх
            check_cust = text("SELECT id FROM customers WHERE phone = :phone")
            customer = conn.execute(check_cust, {"phone": customer_data['phone']}).fetchone()

            if customer:
                customer_id = customer[0]
            else:
                #Шинэ хэрэглэгч үүсгэх
                ins_cust = text("insert into customers (name, phone) values (:name, :phone)")
                res_cust = conn.execute(ins_cust, {
                    "name": customer_data['name'],
                    "phone": customer_data['phone']
                })
                customer_id = res_cust.lastrowid

            # 2. Захиалгыг хадгалах
            ins_order = text("""
                             INSERT INTO orders (customer_id, shipping_address, total_amount, status) 
                             values (:customer_id, :address, :total, 'PENDING')
                             """)
            res_order = conn.execute(ins_order, {
                "customer_id": customer_id,
                "address": customer_data['address'],
                "total": total_amount
            })
            order_id = res_order.lastrowid

            # 3. Захиалгын бараа бүрийг хадгалах
            ins_item = text(""" INSERT INTO order_items(order_id, product_id, quantity, unit_price) values
                             (:order_id, :product_id, :quantity, :unit_price)""")
            
            #Үлдэгдэл шинэчлэх
            upd_stock = text(""" UPDATE products SET quantity = quantity - :qty WHERE id = :product_id """)

            #log бичих
            ins_history = text(""" INSERT INTO log_product_history(product_id, quantity_change, change_type, reason ) VALUES (:product_id, :quantity_change, :change_type, :reason) """)

            for item in card_itmes:
                # Захиалгын барааг нэмэх
                conn.execute(ins_item, {
                    "order_id": order_id,   # захиалгын ID
                    "product_id": item['product_id'], # барааны ID
                    "quantity": item['quantity'], # тоо ширхэг
                    "unit_price": item['price'] # нэгжийн үнэ
                })

                #log бичих
                conn.execute(ins_history, {
                    "product_id": item['product_id'],
                    "quantity_change": -item['quantity'],  # Хасагдаж байгаа тул хасах (-) утга
                    "change_type": "Pending",       # Энэ нь таны 'status' буюу 'change_type'
                    "reason": f"Захиалга #{order_id} үүсэв" # Энэ нь 'reason' хэсэг
                      })

                # Үлдэгдэл шинэчлэх
                conn.execute(upd_stock, {
                    "qty": item['quantity'],
                    "product_id": item['product_id']
                })
                
        return True, "Захиалга амжилттай хадгалагдлаа."
            
    except Exception as e:
                # Хэрэв дээрх үйлдлүүдийн аль нэг дээр алдаа гарвал (жишээ нь тооллого хасаж чадахгүй бол)
                # Систем автоматаар бүх зүйлийг цуцалж (Rollback), энд орж ирнэ.
                return False, str(e)