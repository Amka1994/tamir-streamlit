import streamlit as st
from sqlalchemy import text
import pandas as pd
from highlight.highlight import highlight_low_quantity
from queries.q_product import insert_product, get_all_products
from components.product_dialogs import add_quantity_dialog


def load_products():
    return get_all_products()


def product_page():
    col1, colsp, col2 = st.columns([1, 0.1, 3])

    ########## БАРАА БҮРТГЭЛ ############
    with col1:
        st.markdown("📦 Бараа бүртгэх")
        st.caption("Шинэ бараа системд нэмэх")

        with st.form("product_form", clear_on_submit=True):
            product_name = st.text_input("Барааны нэр")
            product_code = st.text_input("Барааны код")
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
                        st.rerun()
                    else:
                        st.error(f"❌ Алдаа гарлаа: {message}")

    ########## БАРААНЫ ЖАГСААЛТ ############
    with col2:
        st.markdown("🧾 Бүртгэлтэй барааны жагсаалт")

        products = load_products()

        if not products:
                st.info("ℹ️ Одоогоор бүртгэлтэй бараа байхгүй байна.")
        else:
                # DataFrame үүсгэх (id-тай хамт)
                df = pd.DataFrame(
                    products,
                    columns=["id", "🛒 Барааны нэр", "🔖 Барааны код", "🔢 Тоо ширхэг", "📂 Ангилал", "💰 Нэгж үнэ"]
                )

                # None утгыг 0 болгох
                df["🔢 Тоо ширхэг"] = pd.to_numeric(df["🔢 Тоо ширхэг"], errors='coerce').fillna(0).astype(int)
                df["💰 Нэгж үнэ"] = pd.to_numeric(df["💰 Нэгж үнэ"], errors='coerce').fillna(0.0)

                display_df = df[["🛒 Барааны нэр", "🔖 Барааны код", "🔢 Тоо ширхэг", "📂 Ангилал", "💰 Нэгж үнэ"]]

                # Ангиллаар шүүх
                available_categories = sorted(display_df["📂 Ангилал"].dropna().unique())
                if available_categories:
                    selected_categories = st.multiselect(
                        "📂 Ангилалаар шүүх",
                        options=available_categories,
                        default=[],
                        placeholder="Бүгдийг харуулах"
                    )
                    if selected_categories:
                        display_df = display_df[display_df["📂 Ангилал"].isin(selected_categories)]

                                # ШИНЭ: Мөр бүрд "Нэмэх ➕" товчтой жагсаалт
                st.markdown("### 📦 Бараа нэмэх боломжтой жагсаалт")

                for _, row in display_df.iterrows():
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([4, 2, 1.5])

                        with col1:
                            st.subheader(f"{row['🛒 Барааны нэр']} ({row['🔖 Барааны код']})")
                            st.caption(f"🏷️ Ангилал: **{row['📂 Ангилал']}** | 💰 Нэгж үнэ: **{row['💰 Нэгж үнэ']:,} ₮**")

                        with col2:
                            st.metric(
                                label="Нөөцөд байгаа",
                                value=row['🔢 Тоо ширхэг']
                            )

                        with col3:
                            if st.button(
                                "Нэмэх ➕",
                                key=f"add_{row.name}",
                                use_container_width=True,
                                type="primary" if row['🔢 Тоо ширхэг'] < 10 else "secondary"
                            ):
                                # df-с id-г авах (display_df-д id байхгүй)
                                original_row = df.iloc[row.name]
                                add_quantity_dialog(
                                    product_id=original_row["id"],
                                    product_name=original_row["🛒 Барааны нэр"],
                                    current_quantity=original_row["🔢 Тоо ширхэг"]
                                )

                # Доор нэгтгэсэн хүснэгтийг харуулах
                st.markdown("---")
                st.dataframe(
                    display_df.style.apply(highlight_low_quantity, axis=1),
                    use_container_width=True,
                    hide_index=True
                )

                # Нэмэлт статистик
                with st.container(border=True):
                    st.markdown("### 📊 Нийт дүн")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Барааны төрөл", len(display_df))
                    with col2:
                        st.metric("Нийт тоо ширхэг", display_df['🔢 Тоо ширхэг'].sum())
                    with col3:
                        total_value = (display_df['💰 Нэгж үнэ'] * display_df['🔢 Тоо ширхэг']).sum()
                        st.metric("Нийт үнийн дүн", f"{total_value:,.0f} ₮")