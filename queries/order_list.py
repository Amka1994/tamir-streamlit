import logging
import pandas as pd
from sqlalchemy import text

from connection.db import engine

logger = logging.getLogger(__name__)


def get_all_orders() -> "pd.DataFrame":
    ### Бүх захиалгын жагсаалт авах функц

    query = text(""" 
select
    o.id,
    c.name as 'Хэрэлэгч',
    c.phone as 'Утас',
    o.shipping_address as 'Хүргэлтийн хаяг',
    p.name as 'Бараа',
    a.quantity as 'Тоо ширхэг',          
    o.total_amount as 'Нийт дүн',
    o.status as 'Захиалгын статус',
    o.created_at as 'Захиалгын огноо'
from orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items a ON o.id = a.order_id
JOIN products p ON a.product_id = p.id
ORDER BY o.id DESC              
""")
    
    try:
        with engine.connect() as conn:
                # Pandas ашиглан DataFrame болгож авбал Streamlit-д харуулахад хялбар
            df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        logger.exception("get_all_orders алдаа: %s", e)
        return pd.DataFrame()