import streamlit as st

def render_sidebar():
    st.sidebar.title("📦 Sistem Aset")

    st.sidebar.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
    st.sidebar.page_link("pages/2_Input_Aset.py", label="✍️ Input Aset")

    st.sidebar.markdown("---")
    st.sidebar.write(f"👤 {st.session_state.get('user','')}")
