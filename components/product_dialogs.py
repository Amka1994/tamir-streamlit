import streamlit as st
from queries.add_product_quantity import add_product_quantity, remove_product_quantity
from connection.db import engine


#Барааны тоо ширхэг нэмэх диалог
@st.dialog("📦 Барааны гүйлгээ", width="small")
def add_quantity_dialog(product_id: int, product_name: str, current_quantity: int):
    st.write(f"{product_name}")
    st.caption(f"Одоогийн тоо ширхэг: {current_quantity}")

    add_qty = st.number_input("Нэмэх тоо ширхэг", min_value=1, value=1, step=1, key=f"add_qty_{product_id}")
    reason = st.text_area("Тайлбар", max_chars=200, key=f"reason_{product_id}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Нэмэх", use_container_width=True, type="primary", key=f"confirm_add_{product_id}"):
            success, message = add_product_quantity(
                product_id = product_id,
                add_quantity= add_qty,
                reason = reason.strip() or "Тайлбаргүй",
                changed_by = st.session_state.get("username", "system")
            )
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(f"❌ Алдаа гарлаа: {message}")
    with col2:
        if st.button("Болих ❌", use_container_width=True, key=f"cancel_add_{product_id}"):
            st.rerun()

#Барааны тоо ширхэг хасах диалог
@st.dialog("📦 Барааны гүйлгээ", width="small")
def remove_quantity_dialog(product_id: int, product_name: str, current_quantity: int):
    st.write(f"{product_name}")
    st.caption(f"Одоогийн тоо ширхэг: {current_quantity}")

    remove_qty = st.number_input("Хасах тоо ширхэг", min_value=1, value=1, step=1, key=f"remove_qty_{product_id}")
    reason = st.text_area("Тайлбар", max_chars=200, key=f"reason_{product_id}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Хасах", use_container_width=True, type="primary", key=f"confirm_remove_{product_id}"):
            success, message = remove_product_quantity(
                product_id = product_id,
                remove_quantity= remove_qty,
                reason = reason.strip() or "Тайлбаргүй",
                changed_by = st.session_state.get("username", "system")
            )
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(f"❌ Алдаа гарлаа: {message}")
    with col2:
        if st.button("Болих ❌", use_container_width=True, key=f"cancel_add_{product_id}"):
            st.rerun()