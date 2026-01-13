import streamlit as st

def apply_global_filters(df):

    if st.session_state.get("mode") != "dashboard":
        return df

    with st.sidebar:
        st.header("Filter Dashboard")

        # ===== PENYEWA =====
        penyewa_list = sorted(df["penyewa"].dropna().unique())
        penyewa = st.multiselect("Penyewa", penyewa_list)

        if penyewa:
            df = df[df["penyewa"].isin(penyewa)]

        # ===== JENIS ASET =====
        aset_list = sorted(df["jenis_aset"].dropna().unique())
        aset = st.multiselect("Jenis Aset", aset_list)

        if aset:
            df = df[df["jenis_aset"].isin(aset)]

        # ===== TAHUN =====
        tahun_list = sorted(
            df["tahun"]
            .dropna()
            .astype(int)
            .unique()
        )

        tahun = st.multiselect("Tahun SPER", tahun_list)
        st.session_state["tahun_selected"] = tahun

        if tahun:
            df = df[df["tahun"].isin(tahun)]

    return df
