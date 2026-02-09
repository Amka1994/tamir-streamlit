"""
Төвлөрсөн тохиргоо - session state, тогтмолууд, хуудсын нэрс
"""

import streamlit as st

# ---------- Page config ----------
PAGE_TITLE = "Inventory Management System"
PAGE_ICON = "📦"
PAGE_LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# ---------- Session state keys & defaults ----------
SESSION_DEFAULTS = {
    "logged_in": False,
    "show_signup": False,
}

# ---------- Хуудсын цэс ----------
NAV_PAGES = ["Бараа бүртгэл", "Захиалга", "Хүргэлт"]

# ---------- Барааны ангилал ----------
PRODUCT_CATEGORIES = ["Гэр ахуйн", "Хувцас", "Цахилгаан бараа", "Бусад"]

# ---------- Цэсийн загвар ----------
MENU_STYLES = {
    "icon": {"color": "black", "font-size": "18px"},
    "nav-link": {
        "font-size": "14px",
        "text-align": "left",
        "margin": "0px",
        "--hover-color": "#e0e0e0",
    },
    "nav-link-selected": {
        "background-color": "#219ebc",
        "color": "white",
    },
}


def init_session_state():
    """Session state-ийн анхны утгуудыг тохируулах"""
    for key, default in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default
