import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_aset_data
from data_loader import load_master_kantor
from datetime import datetime
import time

# #configurasi
def show_Kantor():
    # sync_session_from_cookie(st.session_state.cookie_manager)
    st.title("🏢 Dashboard SPER Kantor")
# st.title("🏢 Dashboard SPER Kantor")
# st.set_page_config(layout="wide")

    # ======================
    # Realtime Tanggal & Waktu
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

    #definisi nilai uang 
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
    #LOAD DATA
    df = load_aset_data()
    df_master_kantor = load_master_kantor()

    #filter aset
    df = df[df["jenis_aset"] == "Kantor"].copy()

    #====================
    
    # ===================
    #NORMALISASI
    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce").fillna(0)
    df["durasi_bulan"] = pd.to_numeric(df["durasi_bulan"], errors="coerce").fillna(0)

    # ==================
    # FILTER SIDEBAR
    st.header("Filter Kantor")
    a1, a2, a3 = st.columns(3)

    df_filtered = df.copy()  # gunakan df_filtered sebagai df yang difilter

    with a1:
        tahun_list = sorted(df_filtered["tahun"].dropna().astype(int).unique())
        tahun = st.multiselect("Tahun SPER", tahun_list)
        st.session_state["tahun_selected"] = tahun
        if tahun:
            df_filtered = df_filtered[df_filtered["tahun"].isin(tahun)]

    with a2:
        penyewa_list = sorted(df_filtered["penyewa"].dropna().unique())
        penyewa = st.multiselect("Penyewa", penyewa_list)
        if penyewa:
            df_filtered = df_filtered[df_filtered["penyewa"].isin(penyewa)]

    with a3:
        status_list = sorted(df_filtered["status_aset"].dropna().unique())
        status_ = st.multiselect("Status Kantor", status_list)
        if status_:
            df_filtered = df_filtered[df_filtered["status_aset"].isin(status_)]

    st.divider()
    # ===================
    #data sper nomor_surat pages kantor
    df_sper_valid = df[
        df["nomor_surat"].notna() &
        (df["nomor_surat"].str.strip() != " ") &
        (df["nomor_surat"].str.strip() != "") &
        (df["nomor_surat"].str.strip() != "-")    
    ].copy()
    # ================================
    # inisialisai tahun saat ini
    current_year = datetime.now().year
    selected_year = st.session_state.get("tahun_selected")

    if selected_year:
        df_summary = df_sper_valid[df_sper_valid["tahun"].isin(selected_year)].copy()
    else:
        df_summary = df_sper_valid[df_sper_valid["tahun"] == current_year].copy()

    if df_summary.empty:
        st.warning("Tidak ada data SPER untuk tahun yang dipilih")
        st.stop()

    #KPI UTAMA
    df_internal_pal = df_master_kantor[
        df_master_kantor["status_aset"]
        .str.contains("Internal", case=False, na=False)
    ]

    total_sper = df_summary["nomor_surat"].nunique()
    total_nilai = df_summary["nilai"].sum()
    total_luas = df_summary["luas_m2"].median()
    total_sper_internal = df_internal_pal["kode_kantor"].nunique()

    c1, c2, c3, c4= st.columns(4)
    c1.metric("Total SPER", total_sper)
    c2.metric(
        "Ruang Kantor Keperluan Internal PAL",
        total_sper_internal,
        help="Dihitung berdasarkan status 'internal pal' "
    )
    c3.metric("Rata - Rata Luas m2", total_luas)
    c4.metric("Total Nilai Kontribusi (Rp)", format_rupiah_singkat(total_nilai))
    st.caption(f"Nilai sebenarnya: {format_rupiah(total_nilai)}")
    st.divider()
    # ==============
    # ==============
    # Tren SPER
    st.subheader("Tren Nilai Kontribusi SPER per Tahun")
    trend = (
        df_sper_valid
        .groupby("tahun", as_index=False)
        .agg(total_nilai=("nilai", "sum"))
        .sort_values("tahun")
    )
    fig_trend = px.line(
        trend,
        x="tahun",
        y="total_nilai",
        markers=True,
        labels={
            "tahun": "Tahun Mulai SPER",
            "total_nilai": "Total Nilai Kontribusi (Rp)"
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
        tickformat="d"   # penting: tahun tidak pakai koma
    )
    fig_trend.update_yaxes(tickformat=",")
    st.plotly_chart(fig_trend, width="stretch")
    st.divider()

    #=================
    #bar Chart
    st.subheader("Distribusi SPER Kantor Berdasarkan Jumlah dan Kontribusi Penyewa")
    sper_tahun = (
        df_summary
        .groupby("tahun")
        .size()
        .reset_index(name="jumlah")
        .sort_values("tahun")
    )
    fig_year = px.bar(
        sper_tahun,
        x="tahun",
        y="jumlah",
        text="jumlah",
        labels={"tahun": "Tahun", "jumlah": "Jumlah SPER"},
        title= "Jumlah SPER per Tahun"
    )
    fig_year.update_traces(
        textposition="outside",
        hovertemplate=
            "<b>Tahun</b>: %{x}<br>" +
            "<b>Jumlah SPER</b>: %{y}<extra></extra>"
    )
    fig_year.update_xaxes(
        tickmode="linear",
        tickformat="d"
    )
    fig_year.update_layout(height=500)

    # pie chart jumlah
    status_dist = (
        df_summary
        .groupby("status_aset")
        .size()
        .reset_index(name="jumlah")
    )
    fig_status = px.pie(
        status_dist,
        names="status_aset",
        values="jumlah",
        hole=0.4,
        title="Proporsi Jumlah Kondisi Aset Kantor"
    )
    fig_status.update_traces(
        textinfo="percent+label",
        hovertemplate=
            "Status Aset: %{label} <br> Jumlah SPER: %{value}<extra></extra>"
    )
    fig_status.update_layout(height=500)

    col1, col2= st.columns(2)
    with col1:
        st.plotly_chart(fig_year, width="stretch")
    with col2:
        st.plotly_chart(fig_status, width="stretch")
    st.divider()

    # ===================
    # LAYOUT CHART 2
    # Distribusi jumlah ruang kantor 
    st.subheader("Distribusi Jumlah SPER Berdasarkan Lokasi Kantor")
    lokasi_kantor = (
        df_summary
        .groupby("lokasi")["nomor_surat"]
        .size()
        .reset_index(name="jumlah_sper")
        .sort_values("lokasi" , ascending=True)
    )
    fig_bar = px.bar(
        lokasi_kantor,
        x="lokasi",
        y="jumlah_sper",
        color="lokasi",
        text="jumlah_sper",
        labels={
            "lokasi": "Lokasi",
            "jumlah_sper": "Jumlah SPER"
        }
    )
    fig_bar.update_traces(
        textposition="outside",
        hovertemplate="Lokasi: %{x}<br>Jumlah SPER: %{y}<extra></extra>"
    )
    fig_bar.update_layout(height=550)
    st.plotly_chart(fig_bar, width="stretch")
    st.divider()

    #penyewa
    # current_year = datetime.now().year

    # # Jika user tidak memilih filter tahun di sidebar
    # if "tahun" in df.columns:
    #     selected_year = st.session_state.get("tahun_selected")
    # else:
    #     selected_year=None   

    # if not selected_year:
    #     df_chart = df_sper_valid[df_sper_valid["tahun"] == current_year].copy()
    # else: 
    #     df_chart = df_sper_valid[df_sper_valid["tahun"].isin(selected_year)].copy()   
    
    # ==============================
    # Top 10 Penyewa
    st.subheader("Penyewa SPER Berdasarkan Nilai Kontribusi")
    top_penyewa = (
        df_summary
        .groupby("penyewa")["nilai"]
        .sum()
        .reset_index()
        .sort_values("nilai", ascending=False)
        .head(10)
    )
    top_penyewa["label_nilai"] = top_penyewa["nilai"].apply(label_nilai_id)
    top_penyewa["tooltip_nilai"] = top_penyewa["nilai"].apply(format_rupiah_full)
    fig_penyewa = px.bar(
        top_penyewa,
        x="nilai",
        y="penyewa",
        orientation="h",
        text="label_nilai",
        labels={
            "nilai": "Nilai Kontribusi (Rp)",
            "penyewa": "Penyewa"
        }
    )
    fig_penyewa.update_traces(
        textposition="outside",
        hovertemplate=
            "<b>Penyewa</b>: %{y}<br>" +
            "<b>Nilai Kontribusi</b>: %{customdata}<extra></extra>",
        customdata=top_penyewa["tooltip_nilai"]
    )
    fig_penyewa.update_xaxes(
        tickformat=","
    )
    fig_penyewa.update_layout(height=480)
    st.plotly_chart(fig_penyewa, width="stretch")

    #DETAIL TABLE
    # Tabel Detail
    # ======================================================
    st.subheader("📋 Detail SPER Kantor")
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    df["tanggal_mulai"] = df["tanggal_mulai"].apply(format_tanggal_indo)
    df["tanggal_selesai"] = df["tanggal_selesai"].apply(format_tanggal_indo)
    df["nilai_rupiah"] = df["nilai"].apply(format_rupiah)
    st.dataframe(
        df[[
            "nomor_surat",
            "surat_addendum",
            "kode_aset",
            "lokasi",
            "luas_m2",
            "penyewa",
            "pic_num",
            "nilai_rupiah",
            "tanggal_mulai",
            "tanggal_selesai",
            "status_aset"
        ]].rename(columns={
            "nomor_surat": "Nomor Surat",
            "surat_addendum": "SPER Addendum",
            "kode_aset": "Kode Kantor",
            "lokasi": "Lokasi",
            "luas_m2": "Luas (m²)",
            "penyewa": "Penyewa",
            "pic_num": "PIC",
            "nilai_rupiah": "Nilai Kontribusi",
            "tanggal_mulai": "Tanggal Mulai",
            "tanggal_selesai": "Tanggal Selesai",
            "status_aset": "Status"
        }),
        width="stretch"
    )
