import streamlit as st

def show_login(cookie):
    st.title("Login Sistem Aset")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cookie.set("logged_in", "true", key="cookie_logged_in")
        cookie.set("username", username, key="cookie_username")

        st.session_state.is_logged_in = True
        st.session_state.user = username

        st.rerun()
