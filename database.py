import mysql.connector
import streamlit as st

#connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="aset_sper"
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

