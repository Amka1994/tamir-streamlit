import streamlit as st
from sqlalchemy import text
from queries.q_login import login_user

def login_page():
    st.sidebar.subheader("Нэвтрэх")

    with st.sidebar.form("login_form"):
        username = st.text_input("Хэрэглэгчийн нэр")
        password = st.text_input("Нууц үг", type="password")
        submitted = st.form_submit_button("Нэвтрэх", use_container_width=True)

        if submitted:
            if not username or not password:
                st.sidebar.error("Бүх талбарыг бөглөнө үү.")
                return
            success, message, user = login_user(username, password)

            if success:
                st.success(message)
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error(message)