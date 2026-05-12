import streamlit as st

from views.Dashboard_Global import show_Dashboard_Global
from views.Rumdin import show_Rumdin
from views.Kantor import show_Kantor
from views.Kontainer import show_Kontainer
from views.Lahan import show_Lahan
from views.Mess_Menanggal import show_Mess_Menanggal

from input_views.input_rumdin import show as show_Input_Rumdin
from input_views.input_kantor import show as show_Input_Kantor
from input_views.input_kontainer import show as show_Input_Kontainer
from input_views.input_lahan import show as show_Input_Lahan
from input_views.input_mess import show as show_Input_Mess

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

/* Reset semua background */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #f5f7fa !important;
    color: #000000 !important;
}

/* Container utama */
[data-testid="stVerticalBlock"] {
    background: transparent !important;
}

/* Card form */
div[data-testid="stForm"] {
    background: #ffffff !important;
    padding: 2rem !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08) !important;
}

/* Input field */
input, textarea, select {
    background-color: #EEEEEE !important;
    color: #000000 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: #EEEEEE !important;
    color: #000000 !important;
}

/* Number input */
div[data-testid="stNumberInput"] input {
    background-color: #EEEEEE !important;
}

/* Date input */
div[data-testid="stDateInput"] input {
    background-color: #EEEEEE !important;
}

/* Disabled input */
input:disabled {
    background-color: #EEEEEE !important;
    color: #BABABA !important;
}

/* Button */
button {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    border: none !important;
}

button:hover {
    background-color: #1d4ed8 !important;
}

/* Label */
label {
    color: #000000 !important;
    font-weight: 600 !important;
}

/* Caption */
.stCaption {
    color: #6b7280 !important;
}

/* Info / success / error box */
.stAlert {
    background: #f9fafb !important;
    color: #111827 !important;
}

/* Table if any */
table {
    background: #ffffff !important;
    color: #111827 !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"] {display:none;}
</style>
""", unsafe_allow_html=True)

params = st.query_params
page = params.get("page", "global")

if page == "global":
    show_Dashboard_Global()
elif page == "rumdin":
    show_Rumdin()
elif page == "kantor":
    show_Kantor()
elif page == "kontainer":
    show_Kontainer()
elif page == "lahan":
    show_Lahan()
elif page == "mess":
    show_Mess_Menanggal()
elif page == "input_rumdin":
    show_Input_Rumdin()
elif page == "input_kantor":
    show_Input_Kantor()
elif page == "input_kontainer":
    show_Input_Kontainer()
elif page == "input_lahan":
    show_Input_Lahan()
elif page == "input_mess":
    show_Input_Mess()
else:
    show_Dashboard_Global()

