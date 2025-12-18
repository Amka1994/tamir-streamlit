
import streamlit as st
from sqlalchemy import text
from sqlalchemy import create_engine
from urllib.parse import quote_plus



try:
    db_secrets = st.secrets["database"]
except (FileExistsError, KeyError):
    st.warning("secrets.toml олдсонгүй. Локал тохиргоо ашиглаж байна.")
    db_secrets = {
        "host": "localhost",
        "port": "port",
        "user": "user",
        "password": "password",
        "database": "database_name"
    }
password_encoded = quote_plus(db_secrets["password"])
DATABASE_URL = (f"mysql+pymysql://{db_secrets['user']}:{password_encoded}@{db_secrets['host']}:{db_secrets['port']}/{db_secrets['database']}")

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        st.success("Database connection successful.")
    except Exception as e:
        st.error(f"Database connection error: {e}")
     

