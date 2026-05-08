import mysql.connector
import streamlit as st

# connection
def get_connection():
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"]
    )

def fetch(query):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    finally:
        cursor.close()
        conn.close()

    return data, columns