import streamlit as st
import pandas as pd
from queries.q_product import get_all_products
from components.product_card import (init_cart, add_to_cart, remove_from_cart, render_cart)


def product_order():
    st.markdown(" ### 🛒 Бараа захиалах хэсэг")

  
    init_cart() 

    tab1, tab2 = st.tabs(["📦 Захиалга үүсгэх", "🧾 Захиалгын жагсаалт"])

    with tab1:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.caption("Бараа захиалах хэрэглэгчийн мэдээлэл")
            with st.form("order_form", clear_on_submit=True):
                customer_name = st.text_input("Хэрэглэгчийн нэр")
                customer_phone = st.text_input(" 📞 Утасны дугаар")
                customer_phone_2 = st.text_input(" 📞 Нэмэлт утасны дугаар")
                customer_location = st.text_area(" 📍 Хүргэлтийн хаяг")

                submit_order = st.form_submit_button(
                    "✅ Захиалга баталгаажуулах",
                    type="primary"
                )
    
        with col2:
                    st.caption("Бараа сонгох хэсэг")
                    products = get_all_products()

                    product_map = {
                        f"{p[1]} ({p[2]}) - {p[5]:,.0f}₮": p
                        for p in products
                    }

                    selected_label = st.selectbox(
                        "Бүтээгдэхүүн",
                        options=list(product_map.keys()),
                        placeholder="Бүтээгдэхүүн сонгоно уу"
                    )

                    quantity = st.number_input(
                        "🔢 Тоо ширхэг",
                        min_value=1,
                        step=1,
                        value=1
                    )

                    if st.button("➕ Сагсанд нэмэх"):
                        add_to_cart(product_map[selected_label], quantity)
                        st.success("Сагсанд нэмэгдлээ")

             # 🧾 САГС ХАРУУЛАХ
        st.divider()
        total_amount = render_cart()

        # ✅ FORM SUBMIT ДАРАГДСАН ҮЕД
        if submit_order:
            if not st.session_state.cart:
                st.error("Сагс хоосон байна")
            else:
                st.success("🎉 Захиалга баталгаажуулахад бэлэн!")
                # ЭНД:
                # 1. orders insert
                # 2. order_items insert
                # 3. stock хасах   
        





   