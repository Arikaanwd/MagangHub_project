import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_aset_data
from datetime import datetime
import time

#configurasi
def show_Mess_Menanggal():
    st.title("🏨Dashboard SPER Mess Menanggal")

# st.title("🏨Dashboard SPER Mess Menanggal")
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
    
    #definisi nilai uang
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
    def format_rupiah_full(n):
        return f"Rp {n:,.0f}".replace(",", ".")
    def format_tanggal_indo(val):
        if pd.isna(val):
            return ""
        try:
            return val.strftime("%d-%m-%Y")
        except:
            return val
    #===========================
    #load data
    df = load_aset_data()
    #============================
    #filter aset
    df = df[df["jenis_aset"] == "Mess"].copy()
    
    df_all_mess = load_aset_data()
    df_all_mess = df_all_mess[df_all_mess["jenis_aset"] == "Mess"].copy()
    #============================
    #sidebar
    with st.sidebar:
        st.header("Filter Mess Menanggal")

        #tahun
        tahun_list = (
            df["tahun"]
            .dropna()
            .astype(int)
            .unique()
        )
        tahun_list = sorted(tahun_list)

        tahun = st.multiselect("Tahun SPER", tahun_list)
        st.session_state["tahun_selected"] = tahun

        if tahun:
            df = df[df["tahun"].isin(tahun)]
        
        #penyewa
        penyewa_list = sorted (df["penyewa"].dropna().unique())
        penyewa = st.multiselect("penyewa", penyewa_list)

        if penyewa:
            df = df[df["penyewa"].isin(penyewa)]

        # Status
        status_list = sorted(df["status_aset"].dropna().unique())
        status_selected = st.multiselect("Status", status_list)
        if status_selected:
            df = df[df["status_aset"].isin(status_selected)]

        # Sidebar Lantai & Blok
        if "keterangan" in df.columns and not df.empty:
            df["keterangan"] = df["keterangan"].astype(str)

            # Mapping lantai ke kamar
            lantai_mapping = {
                "1": [c for c in "A B C D E F G H".split()] + ["AA","BB","CC","DD","EE","FF","GG","HH"],
                "2": [f"{c}1" for c in "A B C D E F G H".split()] + ["AA1","BB1","CC1","DD1","EE1","FF1","GG1","HH1"],
                "3": [f"{c}2" for c in "A B C D E F G H".split()] + ["AA2","BB2","CC2","DD2","EE2","FF2","GG2","HH2"],
                "4": [f"{c}3" for c in "A B C D E F G H".split()] + ["AA3","BB3","CC3","DD3","EE3","FF3","GG3","HH3"]
            }
            # Daftar lantai unik yang ada di data Mess
            lantai_list = sorted(lantai_mapping.keys())
            lantai_selected = st.multiselect("Lantai", lantai_list)

            # Filter berdasarkan lantai dan kamar
            if lantai_selected:
                kamar_filter = []
                for l in lantai_selected:
                    kamar_filter.extend(lantai_mapping[l])
                df = df[df["keterangan"].isin(kamar_filter)]


    #=====================
    #normalisasi
    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce").fillna(0)
    # df["nilai_perbulan"] = pd.to_numeric(df["nilai_perbulan"], errors="coerce").fillna(0)
    df["durasi_bulan"] = pd.to_numeric(df["durasi_bulan"], errors="coerce").fillna(0)
    
    # ==========================
    # Kolom LANTAI (UNTUK CHART)
    # ==========================
    def get_lantai(kamar):
        for lantai, kamar_list in lantai_mapping.items():
            if kamar in kamar_list:
                return lantai
        return "Tidak Diketahui"

    df["lantai"] = df["keterangan"].astype(str).apply(get_lantai)
    
    #=====================
    #data_sper nomor_surat
    df_sper_valid = df[
        df["nomor_surat"].notna() &
        (df["nomor_surat"].str.strip() != " ") &
        (df["nomor_surat"].str.strip() != "") &
        (df["nomor_surat"].str.strip() != "-")     
    ].copy()
    # ====================
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
    #=====================
    # KPI Metrics
    total_sper = df_chart["nomor_surat"].nunique()
    total_nilai = df_chart["nilai"].sum()
    total_mess = df_all_mess["kode_aset"].nunique()
    rata_nilai = df_chart["nilai"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total SPER", total_sper)
    c2.metric("Total Kamar", total_mess)
    c3.metric("Total Nilai Kontribusi (Rp)", format_rupiah_singkat(total_nilai))
    c4.metric("Rata-rata Nilai per Mess", format_rupiah_singkat(rata_nilai))
    st.caption(f"Nilai sebenarnya: {format_rupiah_full(total_nilai)}")

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
            "tahun": "Tahun SPER",
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

    #=================
    #Distribusi Bar chart dan pie chart
    st.subheader("Distribusi SPER Terhadap Lokasi Unit Kerja Penyewa dan Proporsi Kondisi Aset")
    
    unit_kerja = (
        df_chart
        .groupby("lokasi")["nomor_surat"]
        .size()
        .reset_index(name="jumlah_sper")
        .sort_values("lokasi", ascending=True)
    )
    fig_bar = px.bar(
        unit_kerja,
        x="lokasi",
        y="jumlah_sper",
        labels={
            "lokasi": "Unit Kerja Penyewa",
            "jumlah_sper": "Jumlah SPER"
        },
        title="Distribusi SPER Terhadap Unit Kerja Penyewa"
    )
    fig_bar.update_traces(
        text=unit_kerja["jumlah_sper"],
        textposition="outside",
        hovertemplate="Lokasi: %{x}<br>Jumlah SPER: %{y}<extra></extra>"
    )
    fig_bar.update_layout(height=550)
    

    # pie chart
    status_count = df_chart["status_aset"].value_counts().reset_index()
    status_count.columns = ["status_aset", "Jumlah"]
    fig_status = px.pie(
        status_count,
        names="status_aset",
        values="Jumlah",
        title="Proporsi Kondisi Aset Mess Menanggal"
    )
    fig_status.update_traces(
        textinfo="percent+label",
        hovertemplate="Status Aset: %{label}<br>Jumlah: %{value}<extra></extra>"
    )

    c5, c6 = st.columns([1.8,1])
    with c5:
        st.plotly_chart(fig_bar, width="stretch")
    with c6:
        st.plotly_chart(fig_status, width="stretch")
        
    st.divider()

    # ====================
    # top penyewa
    # ====================
    # current_year = datetime.now().year

    # if "tahun" in df.columns:
    #     selected_year = st.session_state.get("tahun_selected")
    # else:
    #     selected_year=None   

    # if not selected_year:
    #     df_chart = df_sper_valid[df_sper_valid["tahun"] == current_year].copy()
    # else: 
    #     df_chart = df_sper_valid[df_sper_valid["tahun"].isin(selected_year)].copy()   
    
    st.subheader("TOP 10 Penyewa SPER Berdasarkan Nilai Kontribusi")
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
    # =============================
    # barchart lantai
    # ======================
    st.subheader("Distribusi SPER per Lantai Mess Menanggal")
    
    lantai_dist = (
        df_chart
        .groupby("lantai")["nilai"]
        .sum()
        .reset_index()
        .sort_values("lantai", ascending=False)
    )
    top_penyewa["label_nilai"] = top_penyewa["nilai"].apply(label_nilai_id)
    top_penyewa["tooltip_nilai"] = top_penyewa["nilai"].apply(format_rupiah_full)
    
    fig_lantai = px.bar(
        lantai_dist,
        x="lantai",
        y="nilai",
        labels={
            "lantai": "Lantai",
            "nilai": "Nilai Kontribusi (Rp)"
        }
    )
    fig_lantai.update_traces(
        texttemplate="Rp %{y:,.0f}",     
        textposition="outside",
        hovertemplate=
            "<b>Lantai</b>: %{x}<br>" +
            "<b>Nilai Kontribusi</b>: Rp %{y:,.0f}<extra></extra>"
    )
    fig_lantai.update_xaxes(
        tickmode="linear",
        tickformat="d"
    )
    fig_lantai.update_yaxes(tickformat=",")
    fig_lantai.update_layout(height=450)
    st.plotly_chart(fig_lantai, width="stretch")

    st.divider()
    
    # ==================================
    # distribusi tiap lantai pada unit kerja
    #Tampil Data Tabel
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    df["nilai_rupiah"] = df["nilai"].apply(format_rupiah)

    st.subheader("📋Detail SPER Mess Menanggal")
    df["tanggal_mulai_tgl"] = df["tanggal_mulai"].apply(format_tanggal_indo)
    df["tanggal_selesai_tgl"] = df["tanggal_selesai"].apply(format_tanggal_indo)
    st.dataframe(
        df[[
            "nomor_surat",
            "kode_aset",
            "penyewa",
            "lokasi",
            "keterangan",
            "durasi_bulan",
            "nilai_rupiah",
            "tanggal_mulai_tgl",
            "tanggal_selesai_tgl",
            "status_aset"
        ]].rename(columns={
            "nomor_surat": "Nomor Surat",
            "kode_aset": "Kode Aset",
            "penyewa": "Penyewa",
            "lokasi": "Unit Kerja",
            "keterangan": "Blok Kamar",
            "durasi_bulan": "Durasi Sewa",
            "nilai_rupiah": "Nilai Kontribusi (Rp)",
            "tanggal_mulai_tgl": "Tanggal Mulai",
            "tanggal_selesai_tgl": "Tanggal Selesai",
            "status_aset": "Status"
        }),
        width="stretch"
    )


