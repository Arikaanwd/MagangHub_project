import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_aset_data,load_master_lahan
from datetime import datetime
import time


def show_Lahan():
    st.title("🌱 Dashboard SPER Lahan") 
    # st.title("🌱 Dashboard SPER Lahan")     
    # st.set_page_config(layout="wide")

    # ======================
    time_placeholder = st.empty()
    now = datetime.now()
    time_str = now.strftime('%H:%M')
    time_placeholder.markdown(
        f"""
        <div style="text-align:right; font-size:17px; color:gray; margin-bottom:50px;">
            📅 {now.strftime('%d %B %Y')} &nbsp; | &nbsp; {time_str} WIB
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(1)

    def format_rupiah(n):
        return f"Rp {n:,.0f}".replace(",", ".")
    def format_rupiah_singkat(n):
        if n >= 1_000_000_000_000:
            return f"Rp {n/1_000_000_000_000:.2f} T"
        elif n >= 1_000_000_000:
            return f"Rp {n/1_000_000_000:.2f} M"
        elif n >= 1_000_000:
            return f"Rp {n/1_000_000:.2f} jt"
        else:
            return f"Rp {n:,.0f}".replace(",", ".")
    def label_nilai_id(n):
        if n >= 1_000_000_000:
            return f"{n/1_000_000_000:.3f} M".rstrip("0").rstrip(".")
        elif n >= 1_000_000:
            return f"{n/1_000_000:.3f} jt".rstrip("0").rstrip(".")
        else:
            return f"{n:,.0f}".replace(",", ".")
    def format_rupiah_full(n):
        return f"Rp {n:,.0f}".replace(",", ".")
    def format_tanggal_indo(val):
        if pd.isna(val):
            return ""
        try:
            return val.strftime("%d-%m-%Y")
        except:
            return val
        
    # =========================
    df = load_aset_data()
    df_master_lahan = load_master_lahan()

    # =========================
    df = df[df["jenis_aset"] == "Lahan"].copy()
    
    #==========================
    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce").fillna(0)
    df["durasi_bulan"] = pd.to_numeric(df["durasi_bulan"], errors="coerce").fillna(0)
    df["luas_m2"] = pd.to_numeric(df["luas_m2"], errors="coerce").fillna(0)
    
    # =========================
    st.header("Filter Lahan")
    h1, h2, h3 = st.columns(3)
    df_filtered = df.copy()

    with h1:
        tahun_list = sorted(df["tahun"].dropna().astype(int).unique())
        tahun = st.multiselect("Tahun SPER", tahun_list)

        if not tahun:
            tahun = [datetime.now().year]

        df_filtered = df_filtered[df_filtered["tahun"].isin(tahun)]

    with h2:
        penyewa_list = sorted(df_filtered["penyewa"].dropna().unique())
        penyewa = st.multiselect("Penyewa", penyewa_list)

        if penyewa:
            df_filtered = df_filtered[df_filtered["penyewa"].isin(penyewa)]

    with h3:
        status_list = sorted(df_filtered["status_aset"].dropna().unique())
        status_ = st.multiselect("Status Lahan", status_list)

        if status_:
            df_filtered = df_filtered[df_filtered["status_aset"].isin(status_)]

    st.divider()

    # ===================
    df_sper_valid = df[
        df["nomor_surat"].notna() &
        (df["nomor_surat"].str.strip() != "") &
        (df["nomor_surat"].str.strip() != "-")
    ].copy()
    
    # ==================
    # inisialisasi tahun saat ini
    # current_year = datetime.now().year
    # selected_year = st.session_state.get("tahun_selected")

    # if selected_year:
    #     df_filtered = df_sper_valid[df_sper_valid["tahun"].isin(selected_year)].copy()
    # else:
    #     # default: tahun saat ini
    #     df_filtered = df_sper_valid[df_sper_valid["tahun"] == current_year].copy()

    # if df_filtered.empty:
    #     st.warning("Tidak ada data SPER untuk tahun yang dipilih")
    #     st.stop()

    # ==================
    total_sper = df_filtered["kode_aset"].nunique()
    total_luas = df_filtered["luas_m2"].sum()
    total_nilai = df_filtered["nilai"].sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total SPER", total_sper)
    c2.metric("Total Luas Lahan", f"{total_luas:,.0f} m²")
    c3.metric("Total Nilai Kontribusi (Rp)", format_rupiah_singkat(total_nilai))

    st.caption(f"Nilai sebenarnya: {format_rupiah(total_nilai)}")
    st.divider()

    # ==============
    st.subheader("Tren Nilai Kontribusi SPER per Tahun")
    trend = (
        df_sper_valid
        .groupby("tahun", as_index=False)
        .agg(total_nilai=("nilai","sum"))
        .sort_values("tahun")
    )
    fig_trend = px.line(
        trend,
        x="tahun",
        y="total_nilai",
        markers=True,
        labels={
            "tahun": "Tahun Mulai SPER",
            "jumlah_sper": "Total Nilai Kontribusi (Rp)"
        }
    )
    fig_trend.update_traces(
        text=trend["total_nilai"].apply(label_nilai_id),
        textposition="top center",
        mode="lines+markers+text",
        hovertemplate="Tahun: %{x}<br>Rp %{y}<extra></extra>"
    )
    fig_trend.update_xaxes(
        tickmode="linear",
        tickformat="d"
    )
    fig_trend.update_yaxes(tickformat=",")
    st.plotly_chart(fig_trend, width="stretch")
    st.divider()

    # ========================================
    st.subheader("Distribusi Lahan Berdasarkan Luas Tanah dan Kondisi Aset")
    nilai_penyewa = (
        df_filtered
        .groupby("penyewa")["nilai"]
        .sum()
        .reset_index()
    )
    nilai_penyewa["label"] = nilai_penyewa["nilai"].apply(format_rupiah_singkat)
    fig_nilai = px.bar(
        nilai_penyewa.sort_values("nilai"),
        x="penyewa",
        y="nilai",
        color="penyewa",
        text="label",
        labels={
            "penyewa": "Penyewa",
            "nilai": "Nilai Kontribusi (Rp)"
        },
        title= "Nilai Kontribusi Berdasarkan Penyewa"
    )
    fig_nilai.update_traces(
        textposition = "outside",
        hovertemplate="Penyewa: %{x}<br>Nilai Kontribusi: %{y}<extra></extra>"
    )
    fig_nilai.update_layout(
        height=580,
        showlegend=False,
        yaxis_tickformat=","
    )
    fig_nilai.update_layout(height=580)
    st.plotly_chart(fig_nilai, width="stretch")
    st.divider()

    # ======================
    st.subheader("Proporsi Jumlah Kondisi Aset Lahan")

    df_master_lahan["status_aset"] = (
        df_master_lahan["status_aset"]
        .fillna("Kosong")
        .replace("", "Kosong")
        .astype(str)
    )
    kode_aktif = df_filtered["kode_aset"].unique()

    df_status = df_master_lahan[df_master_lahan["kode_lahan"].isin(kode_aktif)]

    status_lahan = (
        df_status
        .groupby("status_aset", dropna=False)
        .size()
        .reset_index(name="jumlah")
    )

    fig_status = px.pie(
        status_lahan,
        names="status_aset",
        values="jumlah",
        hole=0.4
    )
    fig_status.update_traces(
        textinfo="percent+label",
        hovertemplate=
            "Status Aset: %{label}<br> Jumlah SPER: %{value}<extra></extra>"
    )
    fig_status.update_layout(height=500)

    # Luas lahan per Penyewa
    luas_penyewa = (
        df_filtered
        .groupby("penyewa")["luas_m2"]
        .sum()
        .reset_index()
    )
    luas_penyewa["label"] = luas_penyewa["luas_m2"].map(
        lambda x: f"{x:,} m²".replace(",", ".")
    )
    fig_luas = px.bar(
        luas_penyewa.sort_values("luas_m2"),
        x="luas_m2",
        y="penyewa",
        text="label",
        labels={
            "luas_m2": "Luas Lahan (m²)",
            "penyewa": "Penyewa"
        },
        title="Luas Lahan Berdasarkan Penyewa"
    )
    fig_luas.update_traces(
        textposition = "outside",
        hovertemplate="Penyewa: %{y}<br>Luas m²: %{x}<extra></extra>"
    )
    fig_luas.update_layout(height=500)

    c4, c5 = st.columns([1,1.8])
    with c4:
        st.plotly_chart(fig_status, width="stretch")
    with c5:
        st.plotly_chart(fig_luas, width="stretch")

    st.divider()

    # =================================
    st.subheader("📋 Detail SPER Lahan")
    df_filtered = (
        df_filtered
        .sort_values("kode_aset", ascending=True)
        .reset_index(drop=True)
    )
    df_filtered = df_filtered.reset_index(drop=True)
    df_filtered.index = df_filtered.index + 1
    df_filtered["tanggal_mulai"] = df_filtered["tanggal_mulai"].apply(format_tanggal_indo)
    df_filtered["tanggal_selesai"] = df_filtered["tanggal_selesai"].apply(format_tanggal_indo)
    df_filtered["nilai_rupiah"] = df_filtered["nilai"].apply(format_rupiah)

    st.dataframe(
        df_filtered[[
            "nomor_surat",
            "kode_aset",
            "lokasi",
            "luas_m2",
            "penyewa",
            "pic_num",
            "nilai_rupiah",
            "tanggal_mulai",
            "tanggal_selesai",
            "keterangan",
            "status_aset"
        ]].rename(columns={
            "nomor_surat": "Nomor Surat",
            "kode_aset": "Kode Lahan",
            "lokasi": "Lokasi",
            "luas_m2": "Luas (m²)",
            "penyewa": "Penyewa",
            "pic_num": "PIC",
            "nilai_rupiah": "Nilai Kontribusi Pertahun (Rp)",
            "tanggal_mulai": "Tanggal Mulai",
            "tanggal_selesai": "Tanggal Selesai",
            "keterangan": "Keterangan",
            "status_aset": "Status"
        }),
        width="stretch"
    )


