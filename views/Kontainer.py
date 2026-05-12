import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_aset_data , load_master_kontainer
from datetime import datetime
import time

#configurasi
def show_Kontainer():
    st.title("📦 Dashboard SPER Kontainer")
    
    # ======================
    time_placeholder = st.empty()
    now = datetime.now()
    time_str = now.strftime('%H:%M')
    time_placeholder.markdown(
        f"""
        <div style="text-align:right; font-size:17px; color:gray; margin-bottom:50px;">
            📅 {now.strftime('%d %B %Y')} &nbsp
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(1)
    
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
    df = load_aset_data()
    df_master_kontainer = load_master_kontainer()
    df = df[df["jenis_aset"] == "Kontainer"].copy()

    #==================
    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce").fillna(0)
    df["durasi_bulan"] = pd.to_numeric(df["durasi_bulan"], errors="coerce").fillna(0)
    df["volume_feet"] = pd.to_numeric(df["volume_feet"], errors="coerce")
    df["luas_m2"] = pd.to_numeric(df["luas_m2"], errors="coerce")
    df["penyewa_norm"] = (
        df["penyewa"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # ==================
    st.header("Filter Kontainer")
    g1, g2, g3, g4 = st.columns(4)
    df_base = df.copy()

    with g1:
        tahun_list = sorted(df["tahun"].dropna().astype(int).unique())
        tahun = st.multiselect("Tahun SPER", tahun_list)
        if tahun:
            df_base = df_base[df_base["tahun"].isin(tahun)]

    with g2:
        penyewa_list = sorted(df_base["penyewa_norm"].dropna().unique())
        penyewa = st.multiselect("Penyewa", penyewa_list)
        if penyewa:
            df_base = df_base[df_base["penyewa_norm"].isin(penyewa)]

    with g3:
        unit_milik_list = sorted(df_base["keterangan"].dropna().unique())
        unit_milik_selected = st.multiselect("Unit Milik", unit_milik_list)

        if unit_milik_selected:
            df_base = df_base[df_base["keterangan"].isin(unit_milik_selected)]

    with g4:
        volume_list = sorted(df_base["volume_feet"].dropna().unique())
        volume_selected = st.multiselect("Volume (Feet)", volume_list)

        if volume_selected:
            df_base = df_base[df_base["volume_feet"].isin(volume_selected)]

    df_filtered = df_base.copy()

    #==================
    df_sper_valid = df[
        df["nomor_surat"].notna() &
        (df["nomor_surat"].str.strip() != " ") &
        (df["nomor_surat"].str.strip() != "") &
        (df["nomor_surat"].str.strip() != "-") &
        (df["nomor_surat"].str.strip() != "Fasilitas proyek") &
        (df["nomor_surat"].str.strip() != "Digunakan Internal PT PAL")     
    ].copy()

    # =================
    current_year = datetime.now().year
    tahun_dashboard = tahun[0] if tahun else current_year

    df_filtered = df_filtered[df_filtered["tahun"] == tahun_dashboard]
    
    #==================
    total_kontainer = len(df_filtered)
    total_nilai = df_filtered["nilai"].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total SPER", int(total_kontainer))
    c2.metric("SPER Unit 20FT", int((df_filtered["volume_feet"] == 20).sum()))
    c3.metric("SPER Unit 40FT", int((df_filtered["volume_feet"] == 40).sum()))
    c4.metric("Total Nilai Kontribusi", format_rupiah_singkat(total_nilai))
    
    st.caption(f"Nilai sebenarnya: {format_rupiah(total_nilai)}")
    st.divider()

    # ==============
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
    st.subheader("Distribusi SPER Kontainer Berdasarkan Lokasi dan Unit Milik")
    
    c5, c6 = st.columns(2)
    lokasi_kontainer = (
        df_filtered 
        .groupby("lokasi", as_index=False)
        .agg(
            jumlah_sper=("nomor_surat", "count"),
            total_nilai=("nilai", "sum")
        )
    )

    lokasi_kontainer["label_nilai"] = lokasi_kontainer["total_nilai"].apply(label_nilai_id)
    lokasi_kontainer["tooltip_nilai"] = lokasi_kontainer["total_nilai"].apply(format_rupiah_full)

    fig_bar = px.bar(
        lokasi_kontainer,
        x="lokasi",
        y="total_nilai",
        color="lokasi",
        labels={
            "lokasi": "Lokasi",
            "total_nilai": "Nilai Kontribusi (Rp)"
        },
        custom_data=["jumlah_sper"],
        title="Distribusi SPER Berdasarkan Lokasi"
    )
    fig_bar.update_traces(
        texttemplate="Rp %{y:,.0f}",
        textposition="outside",
        hovertemplate=
            "<b>Lokasi</b>: %{x}<br>" +
            "<b>Jumlah SPER</b>: %{customdata[0]}<br>" +
            "<b>Total Nilai</b>: Rp %{y:,.0f}<extra></extra>"
    )
    fig_bar.update_xaxes(
        tickmode="linear",
        tickformat="d"
    )
    fig_bar.update_yaxes(tickformat=",")
    fig_bar.update_layout(height=500)

    # ====================
    volume_dist = (
        df_filtered
        .dropna(subset=["volume_feet"])
        .groupby("volume_feet", as_index=False)
        .agg(
            jumlah_sper=("nomor_surat", "count"),
            total_nilai=("nilai", "sum")
        )
        .sort_values("volume_feet")
    )

    volume_dist["label_nilai"] = volume_dist["total_nilai"].apply(label_nilai_id)
    volume_dist["tooltip_nilai"] = volume_dist["total_nilai"].apply(format_rupiah_full)

    fig_volume_bar = px.bar(
        volume_dist,
        x="volume_feet",
        y="total_nilai",
        color="volume_feet",
        labels={
            "volume_feet": "Volume Kontainer (Feet)",
            "total_nilai": "Nilai Kontribusi (Rp)"
        },
        custom_data=["jumlah_sper"],
        title="Distribusi SPER Kontainer Berdasarkan Volume (Feet)"
    )
    fig_volume_bar.update_traces(
        texttemplate="Rp %{y:,.0f}",  
        textposition="outside",
        hovertemplate=
            "<b>Volume</b>: %{x} feet<br>" +
            "<b>Jumlah SPER</b>: %{customdata[0]}<br>" +
            "<b>Total Nilai</b>: Rp %{y:,.0f}<extra></extra>"
    )
    fig_volume_bar.update_xaxes(
        tickmode="linear",
        tickformat="d"
    )
    fig_volume_bar.update_yaxes(tickformat=",")
    fig_volume_bar.update_layout(
        height=500,
        xaxis=dict(type="category")
    )
    c5.plotly_chart(fig_bar, width="stretch")
    c6.plotly_chart(fig_volume_bar, width="stretch")

    st.divider()

    # =====================
    # kondisi_nilai = (
    #     df_filtered
    #     .groupby("status_aset", as_index=False)
    #     .agg(total_nilai=("nilai", "sum"))
    #     .sort_values("total_nilai", ascending=False)
    # )

    # kondisi_nilai["label_nilai"] = kondisi_nilai["total_nilai"].apply(label_nilai_id)
    # kondisi_nilai["tooltip_nilai"] = kondisi_nilai["total_nilai"].apply(format_rupiah_full)
        
    # fig_kondisi_nilai = px.bar(
    #     kondisi_nilai,
    #     x="status_aset",
    #     y="total_nilai",
    #     color="status_aset",
    #     text="label_nilai",
    #     labels={
    #         "status_aset": "Kondisi Aset",
    #         "total_nilai": "Total Nilai Kontribusi (Rp)"
    #     },
    #     title="Nilai Kontribusi SPER Berdasarkan Kondisi Aset"
    # )

    # fig_kondisi_nilai.update_traces(
    #     textposition="outside",
    #     hovertemplate=
    #         "<b>Kondisi</b>: %{x}<br>" +
    #         "<b>Total Nilai</b>: %{customdata}<extra></extra>",
    #     customdata=kondisi_nilai["tooltip_nilai"]
    # )

    # fig_kondisi_nilai.update_yaxes(tickformat=",")
    # fig_kondisi_nilai.update_layout(height=500)
    # st.plotly_chart(fig_kondisi_nilai, width="stretch")

    # st.divider()

    # ========================
    st.subheader("Penyewa SPER Berdasarkan Nilai Kontribusi")
    top_penyewa = (
        df_filtered
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

    # ================================
    st.subheader("Proporsi Kontainer Berdasarkan Unit Milik dan Kondisi Aset")
    c7, c8 = st.columns(2)
    unit_count = (
        df_filtered
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
    fig_pie.update_layout(height=500)

    # ====================
    df_status_kontainer = df_master_kontainer.copy()
    df_status_kontainer["status_aset"] = (
        df_status_kontainer["status_aset"]
        .astype(str)
        .str.strip()
        .replace("", "Kosong")
    )
    start_year = pd.Timestamp(f"{tahun_dashboard}-01-01")
    end_year   = pd.Timestamp(f"{tahun_dashboard}-12-31")

    df_sewa_tahun = df_filtered[
        (df_filtered["tanggal_mulai"] <= end_year) &
        (df_filtered["tanggal_selesai"] >= start_year)
    ].copy()

    kontainer_disewa = df_sewa_tahun["kode_aset"].unique()

    df_status_kontainer["status_tahun"] = df_status_kontainer["kode_kontainer"].apply(
        lambda x: "Disewa" if x in kontainer_disewa
        else df_status_kontainer.loc[
            df_status_kontainer["kode_kontainer"] == x, "status_aset"
        ].values[0]
    )
    
    df_status_kontainer["status_tahun"] = df_status_kontainer["kode_kontainer"].apply(
        lambda x: "Disewa" if x in kontainer_disewa
        else df_status_kontainer.loc[df_status_kontainer["kode_kontainer"] == x, "status_aset"].values[0]
    )

    kondisi_aset = (
        df_status_kontainer
        .groupby("status_tahun")
        .size()
        .reset_index(name="jumlah_aset")
    )
    fig_kondisi_pie = px.pie(
        kondisi_aset,
        names="status_tahun",
        values="jumlah_aset",
        hole=0.4,
        title=f"Proporsi Kondisi Aset Kontainer Tahun {tahun_dashboard}"
    )
    fig_kondisi_pie.update_traces(
        textinfo="percent+label",
        hovertemplate=
            "Kondisi: %{label}<br>" +
            "Jumlah Aset: %{value}<extra></extra>"
    )
    fig_kondisi_pie.update_layout(height=500)

    c7.plotly_chart(fig_pie, width="stretch")
    c8.plotly_chart(fig_kondisi_pie, width="stretch")
    
    #======================
    df_filtered = (
        df_filtered
        .sort_values("kode_aset", ascending=True)
        .reset_index(drop=True)
    )
    df_filtered["nilai_rupiah"] = df_filtered["nilai"].apply(format_rupiah)

    st.subheader("📋 Detail SPER Kontainer")
    df_filtered["tanggal_mulai_tgl"] = df_filtered["tanggal_mulai"].apply(format_tanggal_indo)
    df_filtered["tanggal_selesai_tgl"] = df_filtered["tanggal_selesai"].apply(format_tanggal_indo)
    df_filtered.index = df_filtered.index + 1

    st.dataframe(
        df_filtered[[
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
            "nilai_rupiah": "Nilai Kontribusi Pertahun (Rp)",
            "tanggal_mulai_tgl": "Tanggal Mulai",
            "tanggal_selesai_tgl": "Tanggal Selesai",
            "keterangan": "Unit Milik",
            "status_aset": "Status"
        }),
        width="stretch"
    )
