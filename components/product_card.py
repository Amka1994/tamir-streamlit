import streamlit as st
import pandas as pd



def init_cart():
    
    # Сагсыг list болгож хадгална
    if "cart" not in st.session_state:
        st.session_state.cart = []


def add_to_cart(product, quantity):
    """product = (id, name, code, quantity, category, price)"""
    for item in st.session_state.cart:
        if item["product_id"] == product[0]:
            item["quantity"] += quantity
            break
    else:  # давхардсан бараа олдоогүй бол шинэ бараа нэмнэ
        st.session_state.cart.append({
            "product_id": product[0],
            "name": product[1],
            "price": product[5],
            "quantity": quantity
        })


def remove_from_cart(product_id):
    st.session_state.cart = [
        item for item in st.session_state.cart
        if item["product_id"] != product_id
    ]


def render_cart():
    st.markdown("### 🧾 Сагс")

    if not st.session_state.cart:
        st.info("Сагс хоосон байна")
        return 0

    df = pd.DataFrame(st.session_state.cart)
    df["subtotal"] = df["price"] * df["quantity"]

    st.dataframe(
        df[["name", "quantity", "price", "subtotal"]].rename(columns={
            "name": "🛒 Бараа",
            "quantity": "🔢 Тоо",
            "price": "💰 Үнэ",
            "subtotal": "💵 Дүн"
        }),
        hide_index=True,
        use_container_width=True
    )

    total = df["subtotal"].sum()
    st.metric("Нийт дүн", f"{total:,.0f} ₮")

    return total
