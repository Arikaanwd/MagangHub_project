import streamlit as st

st.set_page_config(layout="wide")

st.sidebar.title("📊 Sistem Aset")

# ---- DASHBOARD ----
st.sidebar.markdown("### Dashboard")

if st.sidebar.button("📊 Dashboard Global"):
    st.session_state.page = "views/summary_dashboard.py"

if st.sidebar.button("🏢 Kantor"):
    st.session_state.page = "Kantor"

if st.sidebar.button("📦 Kontainer"):
    st.session_state.page = "Kontainer"

if st.sidebar.button("🌱 Lahan"):
    st.session_state.page = "Lahan"

if st.sidebar.button("🏨 Mess Menanggal"):
    st.session_state.page = "Mess_Menanggal"

if st.sidebar.button("🏡Rumah Dinas"):
    st.session_state.page = "Rumdin"


st.sidebar.markdown("---")


# ---- INPUT ----
st.sidebar.markdown("### ✍️ Input Data")

if st.sidebar.button("➕ Input Kantor"):
    st.session_state.page = "input_kantor"

if st.sidebar.button("➕ Input Kontainer"):
    st.session_state.page = "input_kontainer"

if st.sidebar.button("➕ Input Lahan"):
    st.session_state.page = "input_lahan"

if st.sidebar.button("➕ Input Mess"):
    st.session_state.page = "input_mess"

if st.sidebar.button("➕ Input Rumah Dinas"):
    st.session_state.page = "input_rumdin"


# ================= ROUTER =================
# page = st.session_state.page

# if page == "summary_dashboard":
#     show_summary_dashboard()

# elif page == "Kantor":
#     show_Kantor()

# elif page == "Kontainer":
#     show_Kontainer()

# elif page == "Lahan":
#     show_Lahan()

# elif page == "Mess_Menanggal":
#     show_Mess_Menanggal()

# elif page == "Rumdin":
#     show_Rumdin()

# elif page == "input_kantor":
#     input_kantor()

# elif page == "input_kontainer":
#     input_kontainer()

# elif page == "input_lahan":
#     input_lahan()

# elif page == "input_mess":
#     input_mess()

# elif page == "input_rumdin":
#     input_rumdin()
