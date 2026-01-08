import streamlit as st
import pandas as pd

def init_cart():
    if "cart" not in st.session_state:
        st.session_state.cart = []

def add_to_cart(product, quantity):
    """product = (id, name, code, quantity, category, price)"""
    for item in st.session_state.cart:
        if item["product_id"] == product[0]:
            item["quantity"] += quantity
            break
    else:
        st.session_state.cart.append({
            "product_id": product[0],
            "name": product[1],
            "price": product[5],
            "quantity": quantity
        })

# Энэ функцийг шинэчиллээ
def render_cart():
    # st.markdown("🛒 Таны сагс")
    st.caption("🛒 сонгосон бараа")

    if not st.session_state.cart:
        st.info("Сагс хоосон байна")
        return 0

    # 1. Сагсны өгөгдлийг DataFrame болгох
    df = pd.DataFrame(st.session_state.cart)

    # 2. Data Editor ашиглан засварлах боломж олгох
    # num_rows="dynamic" гэснээр хэрэглэгч мөр устгах боломжтой болно
    edited_df = st.data_editor(
        df,
        column_config={
            "product_id": None,  # ID-г хэрэглэгчид харуулахгүй нуух
            "name": st.column_config.Column("🛒 Бараа", disabled=True), # Нэрийг засах боломжгүй
            "price": st.column_config.NumberColumn("💰 Үнэ", format="%d ₮", disabled=True),
            "quantity": st.column_config.NumberColumn("🔢 Тоо", min_value=1, step=1, required=True),
        },
        num_rows="dynamic", # Мөр нэмэх/устгах боломжтой болгох
        use_container_width=True,
        hide_index=True,
        key="cart_editor"
    )

    # 3. Өөрчлөлтийг session_state-д буцааж хадгалах
    # Хэрэглэгч тоог өөрчилсөн эсвэл мөр устгасан бол:
    if len(edited_df) != len(df) or not edited_df.equals(df):
        st.session_state.cart = edited_df.to_dict('records')
        st.rerun()

    # 4. Нийт дүнг тооцоолох
    if not edited_df.empty:
        total = (edited_df["price"] * edited_df["quantity"]).sum()
    else:
        total = 0
        
    st.metric("Нийт дүн", f"{total:,.0f} ₮")

    return total