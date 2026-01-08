import streamlit as st
from connection.db import engine
from queries.q_product import get_all_products
from components.product_card import (init_cart, add_to_cart, render_cart)
from queries.q_order import save_order_complete
from queries.order_list import get_all_orders

# Эцсийн баталгаажуулалт хийх Dialog
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
        # --- ЭНД DATABASE-Д ХАДГАЛАХ ХЭСЭГ ---
        customer_data = {
            'name': name,
            'phone': phone,
            'address': address
        }
        
        # Сагсанд байгаа өгөгдөл: st.session_state.cart
        success, result = save_order_complete(engine, customer_data, st.session_state.cart, total)
        
        if success:
            st.success(f"Захиалга амжилттай хадгалагдлаа! (ID: {result})")
            st.balloons()
            st.session_state.cart = [] # Сагс цэвэрлэх
            st.rerun()
        else:
            st.error(f"Хадгалахад алдаа гарлаа: {result}")

def product_order():
    st.markdown("### 🛒 Бараа захиалах")
    # ТАБҮҮД
    tab1, tab2 = st.tabs(["📦 Бараа захиалага", "🧾 Захиалгын жагсаалт"])
    with tab1:
        init_cart()

        # --- 1. Хэрэглэгчийн мэдээлэл (Нэг мөрөнд) ---
        with st.container(border=True):
            st.caption("👤 Хэрэглэгчийн мэдээлэл")
            c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
            customer_name = c1.text_input("Нэр", placeholder="Нэр", label_visibility="collapsed")
            phone1 = c2.text_input("Утас1", placeholder="Утасны дугаар", label_visibility="collapsed")
            phone2 = c3.text_input("Утас2", placeholder="Нэмэлт дугаар", label_visibility="collapsed")
            customer_location = c4.text_input("📍 Хаяг", placeholder="Хүргэлтийн хаяг", label_visibility="collapsed")

            # Хоёр утсыг нэгтгэх (хэрэв 2 дахь нь байвал)
            full_phone = f"{phone1} / {phone2}" if phone2 else phone1

        coladd, collist = st.columns([1, 1])

        with coladd:
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
                    if st.button("Сагслах", use_container_width=True, type="secondary"):
                        if selected_label:
                            add_to_cart(product_map[selected_label], quantity)
                            st.toast(f"Нэмэгдлээ: {product_map[selected_label][1]}", icon="✅")
                        else:
                            st.error("Бараа сонгоно уу!")
        with collist:
            # --- 3. Сагс (БАЙНГА ХАРАГДАНА) ---
            # st.caption("🛒 Таны сагс")
            # Сагсны хүснэгт энд байна. st.data_editor ашигласан render_cart()
            total_amount = render_cart() 

            # --- 4. Захиалга дуусгах товч ---
            if total_amount > 0:
                st.divider()
                col_space, col_confirm = st.columns([3, 1])
                with col_confirm:
                    if st.button("🚀 Захиалга батлах", type="primary", use_container_width=True):
                        if not customer_name or not phone1:
                            st.error("Хэрэглэгчийн мэдээллийг бүрэн бөглөнө үү!")
                        else:
                            confirm_order_dialog(customer_name, full_phone, customer_location, total_amount)
        
    with tab2:
        st.markdown("### 📋 Захиалгын жагсаалт")
        orders_df = get_all_orders(engine)

        if not orders_df.empty:
        # 2. Хайлтын хэсэг (Сонголттой)
            search_term = st.text_input("🔍 Хайх (Хэрэглэгчийн нэрээр)", "")
            # Анхны утгыг orders_df-ээр авна
            display_df = orders_df

            if search_term:
                display_df = orders_df[orders_df['Хэрэглэгч'].str.contains(search_term, case=False)]
                # 3. Хүснэгтийг харуулах
            st.dataframe(
                        display_df, 
                        use_container_width=True, 
                        hide_index=True
                    )
        else:
            st.info("Одоогоор захиалгын түүх байхгүй байна.")

