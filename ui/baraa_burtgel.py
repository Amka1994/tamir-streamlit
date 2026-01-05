import streamlit as st
import pandas as pd
from highlight.highlight import highlight_low_quantity
from queries.q_product import insert_product, get_all_products, get_product_history
from components.product_dialogs import add_quantity_dialog, remove_quantity_dialog


def load_products():
    return get_all_products()


def product_page():
    st.markdown("# 📦 Бараа бүртгэл")

    # ТАБҮҮД
    tab1, tab2, tab3 = st.tabs(["➕ Бүртгэл", "🧾 Жагсаалт", "📜 Түүх"])

    ########## ТАБ 1: БҮРТГЭЛ ##########
    with tab1:
        st.markdown("### Шинэ бараа бүртгэх")
        st.caption("Системд шинэ бараа нэмэх")

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

            submitted = st.form_submit_button("Бүртгэх", use_container_width=False, type="primary")

            if submitted:
                if not product_name.strip() or not product_code.strip() or product_category is None:
                    st.error("Барааны нэр, код болон ангилалыг заавал бөглөнө үү!")
                else:
                    success, message = insert_product(
                        product_name.strip(),
                        product_code.strip(),
                        int(quantity),
                        product_category,
                        float(price)
                    )
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")

    ########## ТАБ 2: ЖАГСААЛТ ##########
    with tab2:
        st.markdown("### Бүртгэлтэй барааны жагсаалт")

        products = load_products()

        if not products:
            st.info("ℹ️ Одоогоор бүртгэлтэй бараа байхгүй байна.")
        else:
            df = pd.DataFrame(
                products,
                columns=["id", "🛒 Барааны нэр", "🔖 Барааны код", "🔢 Тоо ширхэг", "📂 Ангилал", "💰 Нэгж үнэ"]
            )
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

            # Card-тай жагсаалт
            st.markdown("### Бараа нэмэх/хасах боломжтой жагсаалт")
            for _, row in display_df.iterrows():
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns([4, 2, 1, 1])
                    original_row = df.iloc[row.name]

                    with col1:
                        if st.button(f"{row['🛒 Барааны нэр']} ({row['🔖 Барааны код']})", key=f"detail_{row.name}", use_container_width=True):
                            with st.expander(f"📜 {row['🛒 Барааны нэр']} – Хөдөлгөөний түүх", expanded=True):
                                history = get_product_history(product_id=original_row["id"])
                                if not history:
                                    st.info("Энэ барааны хөдөлгөөн байхгүй байна.")
                                else:
                                    history_df = pd.DataFrame(
                                        history,
                                        columns=["🕒 Огноо", "🔄 Үйлдэл", "🔢 Өөрчлөлт", "⬅️ Өмнөх", "➡️ Шинэ", "📝 Шалтгаан", "👤 Хэн"]
                                    )
                                    history_df["🔄 Үйлдэл"] = history_df["🔄 Үйлдэл"].map({"ADD": "➕ Нэмсэн", "REMOVE": "➖ Хассан", "ADJUST": "🔧 Зассан"})
                                    history_df["🔢 Өөрчлөлт"] = history_df["🔢 Өөрчлөлт"].apply(lambda x: f"+{x}" if x > 0 else str(x))
                                    history_df["🕒 Огноо"] = pd.to_datetime(history_df["🕒 Огноо"]).dt.strftime("%Y-%m-%d %H:%M")
                                    st.dataframe(history_df, use_container_width=True, hide_index=True)

                        st.caption(f"🏷️ Ангилал: **{row['📂 Ангилал']}** | 💰 Үнэ: **{row['💰 Нэгж үнэ']:,} ₮**")

                    with col2:
                        st.metric("Нөөцөд байгаа", row['🔢 Тоо ширхэг'])

                    with col3:
                        if st.button("Нэмэх ➕", key=f"add_{row.name}", use_container_width=True, type="primary"):
                            add_quantity_dialog(
                                product_id=original_row["id"],
                                product_name=original_row["🛒 Барааны нэр"],
                                current_quantity=original_row["🔢 Тоо ширхэг"]
                            )

                    with col4:
                        if st.button("Хасах ➖", key=f"remove_{row.name}", use_container_width=True, type="primary" if row['🔢 Тоо ширхэг'] <= 5 else "secondary"):
                            remove_quantity_dialog(
                                product_id=original_row["id"],
                                product_name=original_row["🛒 Барааны нэр"],
                                current_quantity=original_row["🔢 Тоо ширхэг"]
                            )

            # Нийт дүн
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
            display_history["change_type"] = display_history["change_type"].map({
                "ADD": "➕ Нэмсэн",
                "REMOVE": "➖ Хассан",
                "ADJUST": "🔧 Зассан"
            })
            display_history["quantity_change"] = display_history["quantity_change"].apply(lambda x: f"+{x}" if x > 0 else str(x))

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