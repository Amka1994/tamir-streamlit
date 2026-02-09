import streamlit as st

from queries.q_users import add_user_to_db



def sign_up_user():
    st.sidebar.subheader("Хэрэглэгч нэмэх")

    new_user = st.sidebar.text_input("Хэрэглэгчийн нэр")
    new_password = st.sidebar.text_input("Нууц үг", type="password")
    confirm_password = st.sidebar.text_input("Нууц үг давтах", type="password")

    if st.sidebar.button("Хадгалах"):

        if not new_user or not new_password or not confirm_password:
            st.sidebar.error("Бүх талбарыг бөглөнө үү.")
            return
        
        if new_password != confirm_password:
            st.sidebar.error("Нууц үг таарахгүй байна.")
            return

        # 👉 ЭНД Л DB ФУНКЦ ДУУДНА
        success, message = add_user_to_db(new_user, new_password)

        if success:
            st.sidebar.success(message)
        else:
            st.sidebar.warning(message)
