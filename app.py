import streamlit as st
from data_loader import load_aset_data
from auth.login import show_login
from extra_streamlit_components import CookieManager

# Views Dashboard
from views.Dashboard_Global import show_Dashboard_Global
from views.Kantor import show_Kantor
from views.Kontainer import show_Kontainer
from views.Lahan import show_Lahan
from views.Mess_Menanggal import show_Mess_Menanggal
from views.Rumdin import show_Rumdin

# Input
from input_views.input_home import show as input_home
from input_views.input_kantor import show as input_kantor
from input_views.input_kontainer import show as input_kontainer
from input_views.input_lahan import show as input_lahan
from input_views.input_mess import show as input_mess
from input_views.input_rumdin import show as input_rumdin

st.set_page_config(layout="wide")

# COOKIE
# ======================
cookie = CookieManager()
# ======================
# INIT SESSION DEFAULT
# ======================
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if "mode" not in st.session_state:
    st.session_state.mode = "home"

if "page" not in st.session_state:
    st.session_state.page = None

# ======================
# RESTORE SESSION FROM COOKIE (UNTUK REFRESH SAJA)
# ======================
if not st.session_state.is_logged_in:
    if cookie.get("logged_in") == "true":
        st.session_state.is_logged_in = True
        st.session_state.user = cookie.get("username")
        st.session_state.mode = cookie.get("mode", "home")
        st.session_state.page = cookie.get("page", "Dashboard_Global")

# ======================
# LOGIN GATE (WAJIB)
# ======================
if not st.session_state.is_logged_in:
    show_login(cookie)
    st.stop()
# =====================================================
# Helper untuk Sidebar
# =====================================================
def sidebar_menu(label, page_key):
    is_active = st.session_state.page == page_key

    style = """
        padding:8px 10px;
        border-radius:6px;
        margin-bottom:10px;
        font-weight:600;
        cursor:pointer;
    """
    if is_active:
        style += "background-color:#0051FF;color:white;"
        st.sidebar.markdown(f"<div style='{style}'>{label}</div>", unsafe_allow_html=True)
    else:
        if st.sidebar.button(label):
            st.session_state.page = page_key
            st.rerun()

def hide_sidebar():
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# # =====================================================
# # ❗ LOGIN GATE (PERBAIKAN UTAMA)
# # =====================================================
# if not st.session_state.is_logged_in:
#     show_login(cookie)   # ❗ WAJIB kirim cookie
#     st.stop()

# # =====================================================
# # Inisialisasi Session State
# # =====================================================

# if "is_logged_in" not in st.session_state:
#     st.session_state.is_logged_in = False

# if "mode" not in st.session_state:
#     st.session_state.mode = "home"  # home | dashboard | input

# if "page" not in st.session_state:
#     st.session_state.page = None

# =====================================================
# Sidebar
# =====================================================
st.sidebar.title("Sistem Aset")

if st.session_state.mode == "home":
    if st.sidebar.button("📊 Dashboard Aset"):
        st.session_state.mode = "dashboard"
        st.session_state.page = "Dashboard_Global"
        st.rerun()

    if st.sidebar.button("✍️ Input Aset"):
        st.session_state.mode = "input"
        st.session_state.page = "Input_Home"
        st.rerun()
    
    if st.sidebar.button("Log Out"):
        st.session_state.is_logged_in = False
        st.session_state.mode = "home"
        st.session_state.page = None
        cookie.delete("logged_in")
        cookie.delete("username")
        cookie.delete("mode")
        cookie.delete("page")

        st.rerun()

elif st.session_state.mode == "dashboard":
    st.sidebar.markdown("### 📊 Dashboard Aset")
    sidebar_menu("🔔 Dashboard Global", "Dashboard_Global")
    sidebar_menu("🏠 Rumah Dinas", "Rumdin")
    sidebar_menu("🏢 Kantor", "Kantor")
    sidebar_menu("📦 Kontainer", "Kontainer")
    sidebar_menu("🌱 Lahan", "Lahan")
    sidebar_menu("🏨 Mess Menanggal", "Mess_Menanggal")

    st.sidebar.markdown("---")
    if st.sidebar.button("⬅️ Beranda"):
        st.session_state.mode = "home"
        st.session_state.page = None
        st.rerun()

elif st.session_state.mode == "input":
    st.sidebar.markdown("### ✍️ Input SPER Aset")
    sidebar_menu("📋 Data SPER", "Input_Home")
    sidebar_menu("🏠 Input Rumah Dinas", "Input_Rumdin")
    sidebar_menu("🏢 Input Kantor", "Input_Kantor")
    sidebar_menu("📦 Input Kontainer", "Input_Kontainer")
    sidebar_menu("🌱 Input Lahan", "Input_Lahan")
    sidebar_menu("🏨 Input Mess Menanggal", "Input_Mess")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📒 Input Aset Khusus")
    sidebar_menu("Rumah Dinas","input_rumdin_status")# kantor -> internal
    sidebar_menu("Kantor","input_kantor_status")# rumdin -> internal
    sidebar_menu("Kontainer", "input_kontainer_status")# kontainer -> perbaikan
    sidebar_menu("Lahan", "input_lahan_status")# kontainer -> perbaikan
    sidebar_menu("Mess Menanggal", "input_mess_status")# mess -> perbaikan

    st.sidebar.markdown("---")
    if st.sidebar.button("⬅️ Beranda"):
        st.session_state.mode = "home"
        st.session_state.page = None
        st.rerun()
# =====================================================
# Konten
# =====================================================
if st.session_state.mode == "home":
    hide_sidebar()
    show_Dashboard_Global()

elif st.session_state.mode == "dashboard":
    if st.session_state.page == "Dashboard_Global":
        show_Dashboard_Global()
    elif st.session_state.page == "Rumdin":
        show_Rumdin()
    elif st.session_state.page == "Kantor":
        show_Kantor()
    elif st.session_state.page == "Kontainer":
        show_Kontainer()
    elif st.session_state.page == "Lahan":
        show_Lahan()
    elif st.session_state.page == "Mess_Menanggal":
        show_Mess_Menanggal()

elif st.session_state.mode == "input":
    if st.session_state.page == "Input_Home":
        input_home()
    elif st.session_state.page == "Input_Rumdin":
        input_rumdin()
    elif st.session_state.page == "Input_Kantor":
        input_kantor()
    elif st.session_state.page == "Input_Kontainer":
        input_kontainer()
    elif st.session_state.page == "Input_Lahan":
        input_lahan()
    elif st.session_state.page == "Input_Mess":
        input_mess()
