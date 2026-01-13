import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_aset_data
from datetime import datetime
import time

#configurasi
def show_Kontainer():
    st.title("📦 Dashboard SPER Kontainer")
# st.title("📦 Dashboard SPER Kontainer")
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
    def format_rupiah_full(n):
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
            return f"{n/1_000_000_000:.2f} M"
        elif n >= 1_000_000:
            return f"{n/1_000_000:.2f} jt"
        else:
            return f"{n:,.0f}".replace(",", ".")
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

    #==========================
    #filter aset
    df = df[df["jenis_aset"] == "Kontainer"].copy()

    #==================
    #normalisasi
    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce").fillna(0)
    df["durasi_bulan"] = pd.to_numeric(df["durasi_bulan"], errors="coerce").fillna(0)
    df["volume_feet"] = pd.to_numeric(df["volume_feet"], errors="coerce")
    df["luas_m2"] = pd.to_numeric(df["luas_m2"], errors="coerce")
    df["penyewa_norm"] = (
        df["penyewa"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)  # hapus \r\n & spasi ganda
        .str.strip()
    )

    #==========================
    #sidebar
    with st.sidebar:
        st.header("Filter Kontainer")

        #filter tahun
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

        #filter penyewa
        penyewa_list = sorted(df["penyewa_norm"].dropna().unique())
        penyewa = st.multiselect("penyewa", penyewa_list)

        if penyewa:
            df = df[df["penyewa_norm"].isin(penyewa)]

        # Filter Unit Milik
        unit_milik_list = sorted(df["keterangan"].unique().tolist())
        unit_milik_selected = st.sidebar.multiselect(
            "Unit Milik",
            options=unit_milik_list
        )
        if unit_milik_selected:
            df = df[df["keterangan"].isin(unit_milik_selected)]

        # Filter Volume (Feet)
        volume_list = sorted(df["volume_feet"].unique().tolist())
        volume_selected = st.sidebar.multiselect(
            "Volume (Feet)",
            options=volume_list
        )
        if volume_selected:
            df = df[df["volume_feet"].isin(volume_selected)]

    #==================
    #nomor_surat
    df_sper_valid = df[
        df["nomor_surat"].notna() &
        (df["nomor_surat"].str.strip() != " ") &
        (df["nomor_surat"].str.strip() != "") &
        (df["nomor_surat"].str.strip() != "-") &
        (df["nomor_surat"].str.strip() != "Fasilitas proyek") &
        (df["nomor_surat"].str.strip() != "Digunakan Internal PT PAL")     
    ].copy()

    # =================
    # inisialisasi tahun saat ini
    current_year = datetime.now().year
    selected_year = st.session_state.get("tahun_selected")

    if selected_year and len(selected_year) > 0:
        df_chart = df_sper_valid[df_sper_valid["tahun"].isin(selected_year)].copy()
    else:
        # default: tahun saat ini
        df_chart = df_sper_valid[df_sper_valid["tahun"] == current_year].copy()

    if df_chart.empty:
        st.warning("Tidak ada data SPER Kontainer untuk tahun yang dipilih")
        st.stop()
    #==================
    #KPI
    total_kontainer = len(df_chart)
    total_nilai = df_chart["nilai"].sum()

    rata_volume_feet = (
        df_chart["volume_feet"]
        .replace(0, pd.NA)
        .median()
    )

    rata_luas_m2 = (
        df_chart["luas_m2"]
        .replace(0, pd.NA)
        .median()
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total SPER", int(total_kontainer))
    c2.metric("Rata-rata Volume (Feet)", round(rata_volume_feet, 2))
    c3.metric("Rata-rata Luas (m²)", round(rata_luas_m2, 2))
    c4.metric("Total Nilai Kontribusi", format_rupiah_singkat(total_nilai))
    
    st.caption(f"Nilai sebenarnya: {format_rupiah(total_nilai)}")
    st.divider()

    # ==============
    # Tren SPER
    st.subheader("Tren Nilai Kontribusi SPER per Tahun")
    trend =(
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
            "tahun": "Bulan Mulai SPER",
            "total_nilai": "Jumlah SPER"
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

    #=================
    #Distribusi Bar chart dan pie chart
    st.subheader("Distribusi SPER Kontainer Berdasarkan Lokasi dan Unit Milik")
    
    c5, c6 = st.columns(2)
    lokasi_kontainer = (
        df_chart
        .groupby("lokasi")["nomor_surat"]
        .size()
        .reset_index(name="jumlah_sper")
    )
    fig_bar = px.bar(
        lokasi_kontainer,
        x="lokasi",
        y="jumlah_sper",
        color="lokasi",
        text="jumlah_sper",
        labels={
            "lokasi": "Lokasi",
            "jumlah_sper": "Jumlah SPER"
        },
        title="Distribusi SPER Berdasarkan Lokasi"
    )
    fig_bar.update_traces(
        textposition="outside",
        hovertemplate="Lokasi: %{x}<br>Jumlah SPER: %{y}<extra></extra>"
    )
    fig_bar.update_layout(height=550)

    # pie chart
    unit_count = (
        df_chart
        .groupby("keterangan")
        .size()
        .reset_index(name="jumlah_sper")
    )
    fig_pie = px.pie(
        unit_count,
        names="keterangan",
        values="jumlah_sper",
        hole=0.4,
        title="Proporsi SPER Berdasarkan Unit Milik"
    )
    fig_pie.update_traces(
        textinfo="percent+label",
        hovertemplate="Unit Milik: %{label}<br>Jumlah Data: %{value}<extra></extra>"
    )
    fig_pie.update_layout(height=480)

    c5.plotly_chart(fig_bar, width="stretch")
    c6.plotly_chart(fig_pie, width="stretch")

    st.divider()

    # Kondisi Aset
    st.subheader("Kondisi Aset Kontainer")

    kondisi_aset = (
        df_chart
        .groupby("status_aset")
        .size()
        .reset_index(name="jumlah_aset")
        .sort_values("jumlah_aset", ascending=False)
    )
    fig_kondisi_pie = px.pie(
        kondisi_aset,
        names="status_aset",
        values="jumlah_aset",
        color="status_aset",
        hole=0.4,
        title="Proporsi Kondisi Aset Kontainer"
    )

    fig_kondisi_pie.update_traces(
        textinfo="percent+label",
        hovertemplate=
            "Kondisi: %{label}<br>" +
            "Jumlah Aset: %{value}<extra></extra>"
    )

    fig_kondisi_pie.update_layout(height=450)

    kondisi_nilai = (
        df_chart
        .groupby("status_aset", as_index=False)
        .agg(total_nilai=("nilai", "sum"))
        .sort_values("total_nilai", ascending=False)
    )

    kondisi_nilai["label_nilai"] = kondisi_nilai["total_nilai"].apply(label_nilai_id)
    kondisi_nilai["tooltip_nilai"] = kondisi_nilai["total_nilai"].apply(format_rupiah_full)
        
    fig_kondisi_nilai = px.bar(
        kondisi_nilai,
        x="status_aset",
        y="total_nilai",
        color="status_aset",
        text="label_nilai",
        labels={
            "status_aset": "Kondisi Aset",
            "total_nilai": "Total Nilai Kontribusi (Rp)"
        },
        title="Nilai Kontribusi SPER Berdasarkan Kondisi Aset"
    )

    fig_kondisi_nilai.update_traces(
        textposition="outside",
        hovertemplate=
            "<b>Kondisi</b>: %{x}<br>" +
            "<b>Total Nilai</b>: %{customdata}<extra></extra>",
        customdata=kondisi_nilai["tooltip_nilai"]
    )

    fig_kondisi_nilai.update_yaxes(tickformat=",")
    fig_kondisi_nilai.update_layout(height=500)

    c7, c8 = st.columns(2)
    c7.plotly_chart(fig_kondisi_pie, width="stretch")
    c8.plotly_chart(fig_kondisi_nilai, width="stretch")

    st.divider()
    # ====================
    # volume
    volume_dist = (
        df_chart
        .dropna(subset=["volume_feet"])
        .groupby("volume_feet")
        .size()
        .reset_index(name="jumlah_sper")
        .sort_values("volume_feet")
    )
    fig_volume_bar = px.bar(
        volume_dist,
        x="volume_feet",
        y="jumlah_sper",
        color="volume_feet",
        labels={
            "volume_feet": "Volume Kontainer (Feet)",
            "jumlah_sper": "Jumlah SPER"
        },
        title="Distribusi SPER Kontainer Berdasarkan Volume (Feet)"
    )
    fig_volume_bar.update_traces(
        text=volume_dist["jumlah_sper"],
        textposition="outside",
        hovertemplate=
            "Volume: %{x} feet<br>" +
            "Jumlah SPER: %{y}<extra></extra>"
    )
    fig_volume_bar.update_layout(
        height=480,
        xaxis=dict(type="category")
    )

    st.plotly_chart(fig_volume_bar, width="stretch")
    st.divider()

    # ================================
    # #penyewa
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
    
    # Top 10 Penyewa
    st.subheader("TOP 10 Penyewa SPER Berdasarkan Nilai Kontribusi")
    top_penyewa = (
        df_chart
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

    #======================
    #DETAIL TABLE
    df = (
        df
        .sort_values("kode_aset", ascending=True)
        .reset_index(drop=True)
    )

    df["nilai_rupiah"] = df["nilai"].apply(format_rupiah)

    st.subheader("📋 Detail SPER Kontainer")
    df["tanggal_mulai_tgl"] = df["tanggal_mulai"].apply(format_tanggal_indo)
    df["tanggal_selesai_tgl"] = df["tanggal_selesai"].apply(format_tanggal_indo)
    df.index = df.index + 1

    st.dataframe(
        df[[
            "nomor_surat",
            "kode_aset",
            "lokasi",
            "volume_feet",
            "luas_m2",
            "penyewa",
            "nilai_rupiah",
            "tanggal_mulai_tgl",
            "tanggal_selesai_tgl",
            "keterangan",
            "status_aset"
        ]].rename(columns={  
            "nomor_surat": "Nomor Surat",
            "kode_aset": "Kode Aset",
            "lokasi": "Lokasi",
            "volume_feet": "Volume Feet",
            "luas_m2": "Luas m2",
            "penyewa": "Penyewa",
            "nilai_rupiah": "Nilai Kontribusi (Rp)",
            "tanggal_mulai_tgl": "Tanggal Mulai",
            "tanggal_selesai_tgl": "Tanggal Selesai",
            "keterangan": "Unit Milik",
            "status_aset": "Status"
        }),
        width="stretch"
    )
