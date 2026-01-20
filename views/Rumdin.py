import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_aset_data
from datetime import datetime
import time

#configurasi
def show_Rumdin():
    st.title("🏠 Dashboard SPER Rumah Dinas")
# st.title("🏠 Dashboard SPER Rumah Dinas")
# st.set_page_config(layout="wide")

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

    #definisi nilai rupiah
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
    #load data
    df = load_aset_data()
    # =========================
    #filter aset
    df = df[df["jenis_aset"] == "Rumah Dinas"].copy()
    # ========================
    # ===================
    #normalisasi
    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce").fillna(0)
    df["durasi_bulan"] = pd.to_numeric(df["durasi_bulan"], errors="coerce").fillna(0)
    def normalize_kosong(series, label):
        return (
            series
            .fillna("")
            .astype(str)
            .str.strip()
            .replace("", label)
        )

    df["penyewa"] = normalize_kosong(df["penyewa"], "Belum Ada Penyewa")
    df["status_aset"] = normalize_kosong(df["status_aset"], "Status Tidak Diisi")
    df["keterangan"] = normalize_kosong(df["keterangan"], "Kreditur Tidak Diisi")

    # ===================
    #data sper nomor_surat
    df_sper_valid = df[
        df["nomor_surat"].notna() &
        (df["nomor_surat"].str.strip() != " ") &
        (df["nomor_surat"].str.strip() != "") &
        (df["nomor_surat"].str.strip() != "-")    
    ].copy()
    # ==================
    # inisialisasi tahun saat ini
    current_year = datetime.now().year
    selected_year = st.session_state.get("tahun_selected")

    if selected_year and len(selected_year) > 0:
        df_chart = df_sper_valid[df_sper_valid["tahun"].isin(selected_year)].copy()
    else:
        # default: tahun saat ini
        df_chart = df_sper_valid[df_sper_valid["tahun"] == current_year].copy()

    if df_chart.empty:
        st.warning("Tidak ada data SPER untuk tahun yang dipilih")
        st.stop()
    # ===================
    #KPI
    total_sper = df_chart["nomor_surat"].nunique()
    total_rumah = df["kode_aset"].dropna().str.strip().nunique()
    total_nilai = df_chart["nilai"].sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total SPER", total_sper)
    c2.metric("Total Rumah Dinas", total_rumah)
    c3.metric("Total Nilai Kontribusi (Rp)", format_rupiah_singkat(total_nilai))

    st.caption(f"Nilai sebenarnya: {format_rupiah(total_nilai)}")
    st.divider()

    # =================
    # FILTER
    #sidebar 
    st.header("Filter Rumah Dinas")

    b1,b2,b3,b4 = st.columns(4)

    with b1:
        # Filter Tahun
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
    
    with b2:
        # Filter Penyewa
        penyewa_list = sorted(df["penyewa"].dropna().unique())
        penyewa = st.multiselect("Penyewa", penyewa_list)

        if penyewa:
            df = df[df["penyewa"].isin(penyewa)]
    
    with b3:
        # Filter Kreditur
        kreditur_list = sorted(df["keterangan"].dropna().unique())
        kreditur = st.multiselect("Kreditur", kreditur_list)

        if kreditur:
            df = df[df["keterangan"].isin(kreditur)]
    
    with b4:
        # Filter Status
        status_list = sorted(df["status_aset"].dropna().unique())
        status_ = st.multiselect("Status Rumah", status_list)

        if status_:
            df = df[df["status_aset"].isin(status_)]
    
    st.divider()
    # ==================
    #chart durasi
    st.subheader("Tren Nilai Kontribusi SPER per Tahun")
    trend = (
        df_sper_valid
        .groupby("tahun", as_index=False)
        .agg(total_nilai=("nilai","sum"))
        .sort_values("tahun")
    )
    fig_line = px.line(
        trend,
        x="tahun",
        y="total_nilai",
        markers=True,
        labels={
            "tahun": "Tahun Mulai SPER",
            "total_nilai": "Total Nilai Kontribusi (Rp)"
        }
    )
    fig_line.update_traces(
        text=trend["total_nilai"].apply(label_nilai_id),
        textposition="top center",
        mode="lines+markers+text",
        hovertemplate="Tahun: %{x}<br>Rp %{y}<extra></extra>"
    )
    fig_line.update_xaxes(
        tickmode="linear",
        tickformat="d"
    )
    fig_line.update_yaxes(tickformat=",")
    st.plotly_chart(fig_line, width="stretch")
    st.divider()

    # ==============
    st.subheader("Distribusi Rumah Dinas Berdasarkan Jumlah Data")
    # Count per Kreditur
    dist_kreditur = (
        df_chart
        .groupby("penyewa")
        .size()
        .reset_index(name="jumlah_data")
    )
    # Count per Penyewa
    #bar chart
    dist_penyewa = (
        df_chart
        .groupby("penyewa")
        .size()
        .reset_index(name="jumlah_data")
        .sort_values("jumlah_data", ascending=False)
    )
    fig_bar_count = px.bar(
        dist_penyewa,
        x="penyewa",
        y="jumlah_data",
        labels={
            "penyewa": "Rumah Dinas",
            "jumlah_data": "Jumlah Data"
        },
        title="Jumlah Data Rumah Dinas Berdasarkan Penyewa"
    )
    fig_bar_count.update_traces(
        text=dist_penyewa["jumlah_data"],
        textposition="outside",
        hovertemplate="Rumah Dinas : %{x}<br>Jumlah : %{y}<extra></extra>"
    )
    fig_bar_count.update_layout(height=550)

    #pie chart
    df_status = df_chart.copy()
    # Bersihkan status ringan (tanpa mapping manual)
    df_status["status_aset"] = (
        df_status["status_aset"]
        .astype(str)
        .str.strip()
        .replace("", "Status Tidak Diisi")
    )
    dist_status = (
        df_status
        .groupby("status_aset")
        .size()
        .reset_index(name="jumlah")
        .sort_values("jumlah", ascending=False)
    )
    fig_pie_status = px.pie(
        dist_status,
        names="status_aset",
        values="jumlah",
        hole=0.45,
        title="Proporsi Rumah Dinas Berdasarkan Kondisi Rumah"
    )
    fig_pie_status.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>Status</b>: %{label}<br><b>Jumlah Rumah</b>: %{value}<extra></extra>"
    )

    fig_pie_status.update_layout(height=420)

    c7, c8 = st.columns([1.8,1])
    with c7:
        st.plotly_chart(fig_bar_count, width="stretch")
    with c8:
        st.plotly_chart(fig_pie_status, width="stretch")
    st.divider()
    # ==============
    # bar top penyewa
    # current_year = datetime.now().year

    # if "tahun" in df.columns:
    #     selected_year = st.session_state.get("tahun_selected")
    # else:
    #     selected_year=None   

    # if not selected_year:
    #     df_chart = df_sper_valid[df_sper_valid["tahun"] == current_year].copy()
    # else: 
    #     df_chart = df_sper_valid[df_sper_valid["tahun"].isin(selected_year)].copy()   
    
    st.subheader("TOP 10 Penyewa SPER Berdasrakan Nilai Kontribusi")
    top_penyewa=(
        df_chart
        .groupby("penyewa")["nilai"]
        .sum()
        .reset_index()
        .sort_values("nilai", ascending=True)
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

    st.divider()
    # ==============
    # Bar Chart Penyewa
    st.subheader("Distribusi Alamat Berdasarkan Kondisi Rumah Dinas")
    #bar chart horizontal
    def kelompok_alamat(alamat):
        if not isinstance(alamat, str):
            return "Tidak Diketahui"

        a = alamat.lower()

        if "embong kemiri" in a:
            return "Embong Kemiri"
        elif "darmo permai selatan" in a:
            return "Darmo Permai Selatan"
        elif "darmo permai utara" in a:
            return "Darmo Permai Utara"
        elif "kupang indah" in a:
            return "Kupang Indah"
        elif "kencana sari timur" in a and "kriss" not in a:
            return "Kencana Sari Timur"
        elif "kriss kencana sari timur" in a:
            return "Kriss Kencana Sari Timur"
        elif "siaga raya" in a:
            return "Siaga Raya (Jakarta)"
        elif "paradise" in a:
            return "Paradise (Jakarta)"
        elif "delima timur" in a:
            return "Delima Timur (Jakarta)"
        elif "surabaya" in a:
            return "Surabaya Lainnya"
        elif "jakarta" in a:
            return "Jakarta Lainnya"
        else:
            return "Wilayah Lainnya"

    df_chart["kelompok_alamat"] = df_chart["lokasi"].apply(kelompok_alamat)


    alamat_status = (
        df_chart
        .groupby(["kelompok_alamat", "status_aset"])["lokasi"]
        .nunique()
        .reset_index(name="jumlah_rumah")
    )
    alamat_status["label"] = alamat_status["jumlah_rumah"].astype(str)
    fig_alamat_status = px.bar(
        alamat_status,
        x="kelompok_alamat",
        y="jumlah_rumah",
        color="status_aset",
        custom_data=["status_aset"], 
        barmode="stack",
        text="label",
        labels={
            "kelompok_alamat": "Kelompok Alamat",
            "jumlah_rumah": "Jumlah Rumah Dinas",
            "status_aset": "Status Rumah"
        }
    )

    fig_alamat_status.update_traces(
        textposition="inside",
        insidetextanchor="middle",
        hovertemplate=
            " %{x}<br>" +
            "<b>Status</b>: %{fullData.name}<br>" +
            "<b>Jumlah Rumah</b>: %{y}<extra></extra>"
    )
    fig_alamat_status.update_layout(
        barmode="stack",
        height=560
    )
    st.plotly_chart(fig_alamat_status, width="stretch")
    st.divider()

    # =========================
    #DETAIL TABLE
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    df["nilai_rupiah"] = df["nilai"].apply(format_rupiah)

    st.subheader("📋 Detail SPER Rumah Dinas")
    df["tanggal_mulai_tgl"] = df["tanggal_mulai"].apply(format_tanggal_indo)
    df["tanggal_selesai_tgl"] = df["tanggal_selesai"].apply(format_tanggal_indo)
    st.dataframe(
        df[[
            "nomor_surat",
            "kode_aset",
            "lokasi",
            "penyewa",
            "pic_num",
            "nilai_rupiah",
            "tanggal_mulai_tgl",
            "tanggal_selesai_tgl",
            "keterangan",
            "status_aset"
        ]].rename(columns={
            "nomor_surat": "Nomor Surat",
            "kode_aset": "Kode Aset",
            "lokasi": "Alamat Rumah Dinas",
            "penyewa": "Penyewa",
            "pic_num": "PIC",
            "nilai_rupiah": "Nilai Kontribusi (Rp)",
            "tanggal_mulai_tgl": "Tanggal Mulai",
            "tanggal_selesai_tgl": "Tanggal Selesai",
            "keterangan": "Kreditur",
            "status_aset": "Status"
        }),
        width="stretch"
    )

