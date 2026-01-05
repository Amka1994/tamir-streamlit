import streamlit as st
from ui.login import login_page
from ui.sign_up import sign_up_user
from ui.baraa_burtgel import product_page
from ui.baraa_zahialga import product_order
from streamlit_option_menu import option_menu


st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

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
        page = option_menu(
            "Welcome",
            ["Бараа бүртгэл", "Захиалга", "Хүргэлт"],

            styles={
                "nav-link-selected": {"background-color": "#04AA6D"},
                "icon": {"color": "black", "font-size": "18px"},
                "nav-link": {
                            "font-size": "14px",  # Текстийн хэмжээг багасгасан
                            "text-align": "left",
                            "margin": "0px",
                            "--hover-color": "#e0e0e0"  # Hover үед зөөлөн саарал өнгө
                        },
                        "nav-link-selected": {
                            "background-color": "#219ebc",  # Ногоон өнгө
                            "color": "white"
                        }
            }
        )
    if page == "Бараа бүртгэл":
        product_page()
    
    if page == "Захиалга":
        product_order()
        
    if st.sidebar.button("Log out"):
        st.session_state.clear()
        st.rerun()
