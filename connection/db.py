import pymysql
import streamlit as st



def get_db_connection():
    db = st.secrets["database"]

    return pymysql.connect(
    host=db["host"],
    user=db["user"],
    password=db["password"],
    database=db["database"],
    port=db["port"]
)

