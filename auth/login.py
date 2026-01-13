import streamlit as st
from auth.auth_service import authenticate
from datetime import datetime, timedelta

def show_login(cookie):
    # Render login
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col_left, col_center, col_right = st.columns([1,1,1])

    with col_center:
        st.markdown("<h2 style='text-align:center;'>🔐 Login</h2>", unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Username", label_visibility="collapsed", key="login_username", autocomplete="off")
        password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed", key="login_password", autocomplete="off")

        col1, col2, col3 = st.columns(3)
        with col3:
            if st.button("Login", width='stretch'):
                user = authenticate(username, password)
                if user:
                    expires_at = datetime.now() + timedelta(days=7)

                    # ✅ COOKIE DENGAN KEY UNIK (WAJIB)
                    cookie.set(
                        "logged_in", "true",
                        expires_at=expires_at,
                        key="cookie_logged_in"
                    )
                    cookie.set(
                        "username", username,
                        expires_at=expires_at,
                        key="cookie_username"
                    )
                    cookie.set(
                        "mode", "home",
                        expires_at=expires_at,
                        key="cookie_mode"
                    )
                    cookie.set(
                        "page", "Dashboard_Global",
                        expires_at=expires_at,
                        key="cookie_page"
                    )

                    # ✅ SESSION STATE
                    st.session_state.is_logged_in = True
                    st.session_state.user = username
                    st.session_state.mode = "home"
                    st.session_state.page = "Dashboard_Global"
                    st.rerun() 
                else:
                    st.error("Username atau password salah")
