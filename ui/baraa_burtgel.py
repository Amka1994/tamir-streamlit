import streamlit as st
from sqlalchemy import text
import pandas as pd
from highlight.highlight import highlight_low_quantity
from queries.q_product import insert_product, get_all_products

# ---------- КЭШ ----------
@st.cache_data(ttl=60)  # 60 секунд тутам шинэчлэгдэх боломжтой
def load_products():
    return get_all_products()


def product_page():
    col1, colsp, col2 = st.columns([1, 0.1, 3])

    ########## БАРАА БҮРТГЭЛ ############
    with col1:
        st.markdown("📦 Бараа бүртгэх")
        st.caption("Шинэ бараа системд нэмэх")

        with st.form("product_form", clear_on_submit=True):
            product_name = st.text_input("Барааны нэр", placeholder="Жишээ: Samsung Galaxy S24")
            product_code = st.text_input("Барааны код", placeholder="Жишээ: SAM-S24-001")
            quantity = st.number_input("Тоо ширхэг", min_value=0, value=1, step=1)
            product_category = st.selectbox(
                "Барааны ангилал",
                options=["Гэр ахуйн", "Хувцас", "Цахилгаан бараа", "Бусад"],
                index=None,
                placeholder="Ангилал сонгоно уу"
            )
            price = st.number_input("Нэгж үнэ (₮)", min_value=0.0, value=0.0, step=1000.0, format="%.2f")

            submitted = st.form_submit_button("Бүртгэх", use_container_width=True)

            if submitted:
                # Бүх шаардлагатай талбарыг шалгах
                if not product_name.strip() or not product_code.strip() or product_category is None:
                    st.error("Барааны нэр, код болон ангилалыг заавал бөглөнө үү!")
                elif price < 0 or quantity < 0:
                    st.error("Тоо ширхэг болон үнэ 0-ээс бага байж болохгүй.")
                else:
                    success, message = insert_product(
                        product_name.strip(),
                        product_code.strip(),
                        int(quantity),
                        product_category,
                        float(price)
                    )
                    if success:
                        st.success(f"✅ Амжилттай бүртгэгдлээ: {product_name} ({product_code})")
                        load_products.clear()  # Зөвхөн энэ кэшийг цэвэрлэнэ
                    else:
                        st.error(f"❌ Алдаа гарлаа: {message}")

    ########## БАРААНЫ ЖАГСААЛТ ############
    with col2:
        st.markdown("🧾 Бүртгэлтэй барааны жагсаалт")

        # Кэшийг ашиглан өгөгдөл авах → хурдан бөгөөд серверт ачаалал бага
        products = load_products()

        if not products or len(products) == 0:
            st.info("ℹ️ Одоогоор бүртгэлтэй бараа байхгүй байна.")
            st.stop()  # Цааш код ажиллахгүй, хоосон хуудас үлдэнэ

        # DataFrame үүсгэх
        df = pd.DataFrame(
            products,
            columns=["🛒 Барааны нэр", "🔖 Барааны код", "🔢 Тоо ширхэг", "📂 Ангилал", "💰 Нэгж үнэ"]
        )

        # Ангиллаар шүүх
        available_categories = sorted(df["📂 Ангилал"].dropna().unique().tolist())
        
        if available_categories:
            selected_categories = st.multiselect(
                "📂 Ангилалаар шүүх",
                options=available_categories,
                default=[],
                placeholder="Бүх ангилал"
            )
            if selected_categories:
                df = df[df["📂 Ангилал"].isin(selected_categories)]
        else:
            st.caption("Ангилал байхгүй байна.")

        # Өгөгдлийг хүснэгтээр харуулах + бага тоо ширхэгийг онцлох
        st.dataframe(
            df.style.apply(highlight_low_quantity, axis=1),
            use_container_width=True,
            hide_index=True
        )

        # Нийт тоо, дүнгийн мэдээлэл (нэмэлт боломж)
        with st.expander("📊 Нэмэлт мэдээлэл"):
            st.write(f"**Нийт барааны тоо:** {len(df)}")
            st.write(f"**Нийт үнийн дүн:** {df['💰 Нэгж үнэ'].sum():,.0f} ₮")