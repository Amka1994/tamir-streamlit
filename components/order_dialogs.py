"""Захиалгын диалогууд"""

import streamlit as st

from queries.q_order import save_order_complete


@st.dialog("🚀 Захиалга баталгаажуулах")
def confirm_order_dialog(name: str, phone: str, address: str, total: float) -> None:
    st.warning("Та захиалгыг системд хадгалахдаа итгэлтэй байна уу?")
    st.write(f"**👤 Хэрэглэгч:** {name}")
    st.write(f"**📞 Утас:** {phone}")
    st.write(f"**📍 Хаяг:** {address}")
    st.write(f"**💰 Нийт дүн:** {total:,.0f} ₮")

    st.divider()
    if st.button("✅ Тийм, хадгалах", type="primary", use_container_width=True):
        customer_data = {
            "name": name,
            "phone": phone,
            "address": address,
        }

        success, result = save_order_complete(
            customer_data, st.session_state.cart, total
        )

        if success:
            st.success(f"Захиалга амжилттай хадгалагдлаа! (ID: {result})")
            st.balloons()
            st.session_state.cart = []
            st.rerun()
        else:
            st.error(f"Хадгалахад алдаа гарлаа: {result}")
