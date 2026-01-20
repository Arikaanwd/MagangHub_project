import streamlit as st
from extra_streamlit_components import CookieManager

def require_login():
    cookie = CookieManager()

    # INIT SESSION
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False

    # RESTORE DARI COOKIE
    if not st.session_state.is_logged_in:
        if cookie.get("logged_in") == "true":
            st.session_state.is_logged_in = True
            st.session_state.user = cookie.get("username")

    # GATE
    if not st.session_state.is_logged_in:
        st.error("Silakan login terlebih dahulu")
        st.stop()

    return cookie
