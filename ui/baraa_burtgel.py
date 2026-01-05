import streamlit as st
import pandas as pd
from highlight.highlight import highlight_low_quantity
from queries.q_product import insert_product, get_all_products, get_product_history
from components.product_dialogs import add_quantity_dialog, remove_quantity_dialog


def load_products():
    return get_all_products()


def product_page():
    st.markdown("# 📦 Барааны удирдлага")

    # ТАБҮҮД
    tab1, tab2, tab3 = st.tabs(["📦 Бараа бүртгэл", "🧾 Жагсаалт", "📜 Түүх"])

    ########## ТАБ 1: Бараа үүсгэх ##########
    with tab1:
        col_form, col_income = st.columns([1, 1], gap="large")

        # Зүүн тал: Шинэ бараа бүртгэх
        with col_form:
            st.markdown("### Шинэ бараа үүсгэх")
            st.caption("Системд шинэ бараа үүсгэх")

            with st.form("product_form", clear_on_submit=True):
                product_name = st.text_input("Барааны нэр", placeholder="Жишээ: Samsung Galaxy S24")
                product_code = st.text_input("Барааны код", placeholder="Жишээ: SAM-S24-001")
                product_category = st.selectbox(
                    "Барааны ангилал",
                    options=["Гэр ахуйн", "Хувцас", "Цахилгаан бараа", "Бусад"],
                    index=None,
                    placeholder="Ангилал сонгоно уу"
                )
                price = st.number_input("Нэгж үнэ (₮)", min_value=0.0, value=0.0, step=1000.0, format="%.2f")

                submitted = st.form_submit_button("Бүртгэх", use_container_width=True, type="primary")

                # ЭНД if submitted: дотор байх ёстой!
                if submitted:
                    if not product_name.strip() or not product_code.strip() or product_category is None:
                        st.error("Барааны нэр, код болон ангилалыг заавал бөглөнө үү!")
                    else:
                        success, message = insert_product(
                            product_name.strip(),
                            product_code.strip(),
                            product_category,
                            float(price)
                        )
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")

        # Баруун тал: Татан авалт
        with col_income:
            st.markdown("#### 📥 Татан авалт бүртгэх")
            st.caption("Нийлүүлэгчээс ирсэн барааг ангиллаар шүүж нэмэх")

            # Бараа хайх талбар
            search_query = st.text_input("Барааны код эсвэл нэр хайх", placeholder="Жишээ: SAM-S24-001 эсвэл Galaxy")
            products = load_products()
            if not products:
                st.info("Бүртгэлтэй бараа байхгүй байна.")
            else:
                df = pd.DataFrame(
                    products,
                    columns=["id", "🛒 Барааны нэр", "🔖 Барааны код", "📂 Ангилал", "🔢 Тоо ширхэг", "💰 Нэгж үнэ"]
                )


                # Хайлт хийх
                if search_query.strip():
                    search_lower = search_query.strip().lower()
                    matched = df[
                        df["🔖 Барааны код"].str.lower().str.contains(search_lower, na=False) |
                        df["🛒 Барааны нэр"].str.lower().str.contains(search_lower, na=False)
                    ]

                    if matched.empty:
                        st.info("Ийм код эсвэл нэртэй бараа олдсонгүй.")
                    else:
                        # Зөвхөн таарсан бараануудыг харуулах
                        for _, row in matched.iterrows():
                            with st.container(border=True):
                                col_info, col_action = st.columns([3, 2])

                                with col_info:
                                    st.write(f"**{row['🛒 Барааны нэр']}**")
                                    st.caption(f"Код: {row['🔖 Барааны код']} | Ангилал: {row['📂 Ангилал']} | Одоогийн тоо: **{row['🔢 Тоо ширхэг']}**")

                                with col_action:
                                    col_add, col_remove = st.columns(2)
                                    with col_add:
                                        if st.button("Нэмэх ➕", key=f"add_{row['id']}", use_container_width=True, type="primary"):
                                            add_quantity_dialog(
                                                product_id=row["id"],
                                                product_name=row["🛒 Барааны нэр"],
                                                current_quantity=row["🔢 Тоо ширхэг"]
                                            )

                                    with col_remove:
                                        if st.button("Хасах ➖", key=f"remove_{row['id']}", use_container_width=True, type="primary"):
                                            remove_quantity_dialog(
                                                product_id=row["id"],
                                                product_name=row["🛒 Барааны нэр"],
                                                current_quantity=row["🔢 Тоо ширхэг"]
                                            )
    ########## ТАБ 2: ЖАГСААЛТ ##########
    with tab2:
        st.markdown("### Бүртгэлтэй барааны жагсаалт")

        products = load_products()

        if not products:
            st.info("ℹ️ Одоогоор бүртгэлтэй бараа байхгүй байна.")
        else:
            df = pd.DataFrame(
                products,
                columns=["id", "name", "code", "quantity", "category", "price"])

            df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
            df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0.0)

            # Ангиллаар шүүх
            available_categories = sorted(df["category"].dropna().unique())
            selected_categories = st.multiselect(
                    "📂 Ангилалаар шүүх",
                    options=available_categories,
                    default=[],
                    placeholder="Бүгдийг харуулах"
                )

            # Барааны жагсаалт харуулах
            display_df = df.copy()
            if selected_categories:
                    display_df = display_df[display_df["category"].isin(selected_categories)]

            st.dataframe(
                display_df.rename(columns={
                    "name": "🛒 Барааны нэр",
                    "code": "🔖 Барааны код",
                    "quantity": "🔢 Тоо ширхэг",
                    "category": "📂 Ангилал",
                    "price": "💰 Нэгж үнэ"
                })[["🛒 Барааны нэр", "🔖 Барааны код", "🔢 Тоо ширхэг", "📂 Ангилал", "💰 Нэгж үнэ"]],
                use_container_width=True,
                hide_index=True
            )

            # # Нийт дүн
            # with st.container(border=True):
            #     st.markdown("### 📊 Нийт дүн")
            #     col1, col2, col3 = st.columns(3)
            #     with col1:
            #         st.metric("Барааны төрөл", len(display_df))
            #     with col2:
            #         st.metric("Нийт тоо ширхэг", display_df['🔢 Тоо ширхэг'].sum())
            #     with col3:
            #         total_value = (display_df['💰 Нэгж үнэ'] * display_df['🔢 Тоо ширхэг']).sum()
            #         st.metric("Нийт үнийн дүн", f"{total_value:,.0f} ₮")

        ########## ТАБ 3: ТҮҮХ ##########
    with tab3:
        st.markdown("### 📜 Барааны хөдөлгөөний түүх")

        # Бүх түүхийг авна
        history = get_product_history()

        if not history:
            st.info("ℹ️ Одоогоор ямар ч хөдөлгөөн байхгүй байна.")
            st.stop()

        # DataFrame болгох
        history_df = pd.DataFrame(
            history,
            columns=["changed_at", "product_name", "change_type", "quantity_change", "previous_quantity", "new_quantity", "reason", "changed_by"]
        )
        history_df["changed_at"] = pd.to_datetime(history_df["changed_at"])

        # Хамгийн эртний болон хамгийн сүүлийн огноог олох
        min_date = history_df["changed_at"].min().date()
        max_date = history_df["changed_at"].max().date()

        # Огнооны шүүлт
        col_from, col_to = st.columns(2)
        with col_from:
            start_date = st.date_input("Эхлэх огноо", value=min_date, min_value=min_date, max_value=max_date)
        with col_to:
            end_date = st.date_input("Дуусах огноо", value=max_date, min_value=min_date, max_value=max_date)

        # Шүүх
        filtered_df = history_df[
            (history_df["changed_at"].dt.date >= start_date) &
            (history_df["changed_at"].dt.date <= end_date)
        ]

        if filtered_df.empty:
            st.info(f"{start_date} - {end_date} хооронд хөдөлгөөн байхгүй байна.")
        else:
            display_history = filtered_df.copy()
            display_history["changed_at"] = display_history["changed_at"].dt.strftime("%Y-%m-%d %H:%M")

            # 1️⃣ Эхлээд quantity-г format хийнэ
            def format_quantity(row):
                if row["change_type"] == "ADD":
                    return f"+{abs(row['quantity_change'])}"
                elif row["change_type"] == "REMOVE":
                    return f"-{abs(row['quantity_change'])}"
                else:  # ADJUST эсвэл бусад
                    return str(row["quantity_change"])
            
            display_history["quantity_change"] = display_history.apply(
                format_quantity, axis=1
            )
                
            display_history["change_type"] = display_history["change_type"].map({
                "ADD": "Нэмсэн",
                "REMOVE": "Хассан",
                "ADJUST": "Зассан"
            })

            

            st.dataframe(
                display_history[["changed_at", "product_name", "change_type", "quantity_change", "previous_quantity", "new_quantity", "reason", "changed_by"]].rename(columns={
                    "changed_at": "🕒 Огноо",
                    "product_name": "🛒 Бараа",
                    "change_type": "🔄 Үйлдэл",
                    "quantity_change": "🔢 Өөрчлөлт",
                    "previous_quantity": "⬅️ Өмнөх",
                    "new_quantity": "➡️ Шинэ",
                    "reason": "📝 Шалтгаан",
                    "changed_by": "👤 Хэн"
                }),
                use_container_width=True,
                hide_index=True
            )