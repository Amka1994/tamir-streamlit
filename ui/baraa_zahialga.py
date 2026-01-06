import streamlit as st
from queries.q_product import get_all_products
from components.product_card import (init_cart, add_to_cart, render_cart)

# Эцсийн баталгаажуулалт хийх Dialog
@st.dialog("🚀 Захиалга баталгаажуулах")
def confirm_order_dialog(name, phone, address, total):
    st.warning("Та захиалгыг системд хадгалахдаа итгэлтэй байна уу?")
    st.write(f"**👤 Хэрэглэгч:** {name}")
    st.write(f"**📞 Утас:** {phone}")
    st.write(f"**📍 Хаяг:** {address}")
    st.write(f"**💰 Нийт дүн:** {total:,.0f} ₮")
    
    st.divider()
    if st.button("✅ Тийм, хадгалах", type="primary", use_container_width=True):
        # Энд Database-д хадгалах функцээ дуудна
        # save_order_to_db(name, phone, address, st.session_state.cart)
        
        st.success("Захиалга амжилттай хадгалагдлаа!")
        st.session_state.cart = [] # Сагс цэвэрлэх
        st.rerun()

def product_order():
    st.markdown("### 🛒 Бараа захиалах")
    init_cart()

    # --- 1. Хэрэглэгчийн мэдээлэл (Нэг мөрөнд) ---
    with st.container(border=True):
        st.caption("👤 Хэрэглэгчийн мэдээлэл")
        c1, c2, c3 = st.columns([1, 1, 2])
        customer_name = c1.text_input("Нэр", placeholder="Нэр", label_visibility="collapsed")
        customer_phone = c2.text_input("Утас", placeholder="Утасны дугаар", label_visibility="collapsed")
        customer_location = c3.text_input("📍 Хаяг", placeholder="Хүргэлтийн хаяг", label_visibility="collapsed")

    # --- 2. Бараа сонгох (Нэг мөрөнд) ---
    st.write("##")
    products = get_all_products()
    product_map = {f"{p[1]} ({p[2]}) - {p[5]:,.0f}₮": p for p in products}

    with st.container(border=True):
        st.caption("📦 Бараа нэмэх")
        col_prod, col_qty, col_add = st.columns([3, 1, 1])
        with col_prod:
            selected_label = st.selectbox("Бараа", options=list(product_map.keys()), label_visibility="collapsed", index=None, placeholder="Бараа сонгох...")
        with col_qty:
            quantity = st.number_input("Тоо", min_value=1, value=1, label_visibility="collapsed")
        with col_add:
            if st.button("➕ Нэмэх", use_container_width=True, type="secondary"):
                if selected_label:
                    add_to_cart(product_map[selected_label], quantity)
                    st.toast(f"Нэмэгдлээ: {product_map[selected_label][1]}", icon="✅")
                else:
                    st.error("Бараа сонгоно уу!")

    # --- 3. Сагс (БАЙНГА ХАРАГДАНА) ---
    st.write("##")
    # Сагсны хүснэгт энд байна. st.data_editor ашигласан render_cart()
    total_amount = render_cart() 

    # --- 4. Захиалга дуусгах товч ---
    if total_amount > 0:
        st.divider()
        col_space, col_confirm = st.columns([3, 1])
        with col_confirm:
            if st.button("🚀 Захиалга батлах", type="primary", use_container_width=True):
                if not customer_name or not customer_phone:
                    st.error("Хэрэглэгчийн мэдээллийг бүрэн бөглөнө үү!")
                else:
                    confirm_order_dialog(customer_name, customer_phone, customer_location, total_amount)