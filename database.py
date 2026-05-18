import mysql.connector
import streamlit as st


def get_connection():
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        port=int(st.secrets["DB_PORT"]),
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"],
        connection_timeout=30
    )


def fetch(query):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)

        data = cursor.fetchall()

        columns = [i[0] for i in cursor.description]

        return data, columns

    except Exception as e:
        st.error(f"Database error: {e}")
        return [], []

    finally:
        cursor.close()
        conn.close()