import streamlit as st

# Fungsi untuk menyinkronisasi session_state dari cookie
def sync_session_from_cookie(cookie):
    """
    Sync session_state dari cookie.
    Harus dipanggil di awal setiap halaman sebelum render konten.
    """
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "mode" not in st.session_state:
        st.session_state.mode = "home"
    if "page" not in st.session_state:
        st.session_state.page = None

    # Baca cookie (instance cookie di-inject dari app.py)
    try:
        logged_in_cookie = cookie.get("logged_in")
        username_cookie = cookie.get("username")
        mode_cookie = cookie.get("mode")
        page_cookie = cookie.get("page")

        if logged_in_cookie == "true" and username_cookie:
            st.session_state.logged_in = True
            st.session_state.user = username_cookie

        if mode_cookie:
            st.session_state.mode = mode_cookie
        if page_cookie:
            st.session_state.page = page_cookie
    except Exception:
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.mode = "home"
        st.session_state.page = None
