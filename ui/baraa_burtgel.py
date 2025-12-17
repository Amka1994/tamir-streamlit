import streamlit as st
from sqlalchemy import text
import pandas as pd
from highlight.highlight import highlight_low_quantity
from queries.q_product import insert_product, get_all_products


def product_page():

 ########## БАРАА БҮРТГЭЛ ############
    col1, colsp, col2 = st.columns([1, 0.1, 3])
    with col1:
        st.markdown("📦 Бараа бүртгэх")
        st.caption("Шинэ бараа системд нэмэх")
        with st.form("product_form", clear_on_submit=True):
            product_name = st.text_input("Барааны нэр")
            product_code = st.text_input("Барааны код")
            quantity = st.number_input("Тоо ширхэг")
            product_category = st.selectbox("Барааны ангилал", ["Гэр ахуйн", "Хувцас", "Цахилгаан бараа", "Бусад"], index=None, placeholder="Төрөл сонгоно уу")
            price = st.number_input("Үнэ")

            submitted = st.form_submit_button("Бүртгэх", use_container_width=True)

            if submitted:
                if not product_name or not product_code:
                    st.error("Бүх талбарыг бөглөнө үү.")
                else:
                    success, message = insert_product(
                        product_name,
                        product_code,
                        quantity,
                        product_category,
                        price
                    )
                    if success:
                        st.success(f"Бараа амжилттай бүртгэгдлээ: {product_name} ({product_code}) - {quantity} ширхэг, Ангилал: {product_category}")
                        st.rerun()
                    else:
                        st.error(message)

                

     ########## БАРААНЫ ЖАГСААЛТ ############
    with col2:
        st.markdown("🧾 Бүртгэлтэй барааны жагсаалт")

        products = get_all_products()

        if not products:
            st.info("Одоогоор бүртгэлтэй бараа байхгүй байна.")
        else:
            df = pd.DataFrame(
        products,
        columns=["🛒 Барааны нэр", " 🔖 Барааны код", "🔢 Тоо ширхэг", "📂 Ангилал", "💰 Нэгж үнэ"])
        #st.dataframe(df.style.apply(highlight_low_quantity, axis=1), use_container_width=True, hide_index=True)


        ########## Ангилалаар хайх ############

        categories = sorted(df["📂 Ангилал"].unique().tolist())

        selected_category = st.multiselect("Ангилалаар шүүх", categories)

        if selected_category:
            df = df[df["📂 Ангилал"].isin(selected_category)]

        st.dataframe(
            df.style.apply(highlight_low_quantity, axis=1),
            use_container_width=True,
            hide_index=True
        )

    
            
        
            
        
