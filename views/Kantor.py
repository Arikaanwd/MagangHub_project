import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_aset_data
from data_loader import load_master_kantor
from datetime import datetime
import time


def show_Kantor():
    st.title("🏢 Dashboard SPER Kantor")
    # st.title("🏢 Dashboard SPER Kantor")
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
    df_master_kantor = load_master_kantor()
    df = df[df["jenis_aset"] == "Kantor"].copy()

    # ===================
    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce").fillna(0)
    df["durasi_bulan"] = pd.to_numeric(df["durasi_bulan"], errors="coerce").fillna(0)
    df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce").fillna(0).astype(int)
    
    # ==================
    st.header("Filter Kantor")
    a1, a2, a3 = st.columns(3)
    df_filtered = df.copy()
    
    with a1:
        tahun_list = sorted(df["tahun"].dropna().unique())
        tahun = st.multiselect("Tahun SPER", tahun_list)

        if not tahun:
            tahun = [datetime.now().year] 

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
    
    # ===================
    df_sper_valid = df[
        df["nomor_surat"].notna() &
        (df["nomor_surat"].str.strip() != " ") &
        (df["nomor_surat"].str.strip() != "") &
        (df["nomor_surat"].str.strip() != "-")    
    ].copy()
    
    # ==================
    df_summary = df_filtered.copy()

    if df_summary.empty:
        st.warning("Tidak ada data sesuai filter")
        st.stop()

    df_internal_pal = df_master_kantor[
        df_master_kantor["status_aset"]
        .str.contains("Internal", case=False, na=False)
    ]

    total_sper = df_summary["kode_aset"].nunique()
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
        tickformat="d" 
    )
    fig_trend.update_yaxes(tickformat=",")
    st.plotly_chart(fig_trend, width="stretch")
    st.divider()

    # ===================
    st.subheader("Distribusi Jumlah SPER Berdasarkan Lokasi Kantor")
    lokasi_kantor = (
        df_summary
        .groupby("lokasi",as_index=False)
        .agg(
            jumlah_sper=("nomor_surat", "size"),
            total_nilai=("nilai", "sum")
        )
        .sort_values("lokasi" , ascending=True)
    )
    lokasi_kantor["label_nilai"]=lokasi_kantor["total_nilai"].apply(label_nilai_id)
    lokasi_kantor["tooltip_nilai"]=lokasi_kantor["total_nilai"].apply(format_rupiah_full)

    fig_bar = px.bar(
        lokasi_kantor,
        x="lokasi",
        y="total_nilai",
        color="lokasi",
        labels={
            "lokasi": "Lokasi",
            "total_nilai": "Nilai Kontribusi (Rp)"
        },
        custom_data=["jumlah_sper"]
    )
    fig_bar.update_traces(
        texttemplate="Rp %{y:,.0f}",  
        textposition="outside",
        hovertemplate="Lokasi: %{x}<br>Jumlah SPER: %{customdata[0]}<br>Nilai Kontribusi: Rp %{y:,.0f}<extra></extra>",
    )
    fig_bar.update_xaxes(
        tickmode="linear",
        tickformat="d"
    )
    fig_bar.update_yaxes(tickformat=",")
    fig_bar.update_layout(height=550)
    st.plotly_chart(fig_bar, width="stretch")
    st.divider()

    # ===============
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
    st.divider()

    #=================
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
    # =============
    df_status = df_master_kantor.copy()
    df_status["status_aset"] = (
        df_status["status_aset"]
        .fillna("Kosong")
        .replace("", "Kosong")
        .astype(str)
        .str.strip()
    )

    kode_terpakai = df_summary["kode_aset"].unique()
    df_status = df_status[df_status["kode_kantor"].isin(kode_terpakai)]

    status_dist = (
        df_status
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
            "Status Aset: %{label} <br> Jumlah: %{value}<extra></extra>"
    )
    fig_status.update_layout(height=500)

    col1, col2= st.columns(2)
    with col1:
        st.plotly_chart(fig_year, width="stretch")
    with col2:
        st.plotly_chart(fig_status, width="stretch")
    st.divider()

    # ====================================
    st.subheader("📋 Detail SPER Kantor")
    df_summary = df_summary.reset_index(drop=True)
    df_summary.index = df_summary.index + 1
    df_summary["tanggal_mulai"] = df_summary["tanggal_mulai"].apply(format_tanggal_indo)
    df_summary["tanggal_selesai"] = df_summary["tanggal_selesai"].apply(format_tanggal_indo)
    df_summary["nilai_rupiah"] = df_summary["nilai"].apply(format_rupiah)
    st.dataframe(
        df_summary[[
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
