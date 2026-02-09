import streamlit as st
from streamlit_option_menu import option_menu

from config import (
    MENU_STYLES,
    NAV_PAGES,
    PAGE_ICON,
    PAGE_LAYOUT,
    PAGE_TITLE,
    SIDEBAR_STATE,
    init_session_state,
)
from ui.baraa_burtgel import product_page
from ui.baraa_zahialga import product_order
from ui.login import login_page
from ui.sign_up import sign_up_user

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE,
)

# ---------------- SESSION INIT ----------------
init_session_state()

# ---------------- BEFORE LOGIN ----------------
if not st.session_state.logged_in:

    if st.session_state.show_signup:
        sign_up_user()

        if st.sidebar.button("⬅ Back to Login"):
            st.session_state.show_signup = False
            st.rerun()
    else:
        login_page()

        if st.sidebar.button("Sign Up"):
            st.session_state.show_signup = True
            st.rerun()

# ---------------- AFTER LOGIN ----------------
else:
    st.sidebar.success(f"Нэвтэрсэн: {st.session_state.user['username']}")
    with st.sidebar:
        page = option_menu("Welcome", NAV_PAGES, styles=MENU_STYLES)

    if page == NAV_PAGES[0]:  # Бараа бүртгэл
        product_page()
    
    if page == NAV_PAGES[1]:  # Захиалга
        product_order()

    if page == NAV_PAGES[2]:  # Хүргэлт
        st.info("🚚 Хүргэлтийн хуудас хөгжүүлэгдэж байна...")
        
    if st.sidebar.button("Log out"):
        st.session_state.clear()
        st.rerun()
