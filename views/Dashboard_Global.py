import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_aset_data
from filters import apply_global_filters
from datetime import datetime
import time
import folium 
from streamlit_folium import st_folium
from maps.leaflet_maps import render_map

# ===== Cek login di awal =====
# sync_session_from_cookie(cookie)
# ======================
def show_Dashboard_Global():
    # sync_session_from_cookie(st.session_state.cookie_manager)
    st.title("🔔 Dashboard Global Aset")
# st.title("🔔 Dashboard Global Aset")
# st.set_page_config(layout="wide")

    # ======================
    # Realtime Tanggal & Waktu
    # ======================
    time_placeholder = st.empty()
    now = datetime.now()
    time_str = now.strftime('%H:%M')
    time_placeholder.markdown(
        f"""
        <div style="text-align:right; font-size:17px; color:gray;">
            📅 {now.strftime('%d %B %Y')} &nbsp; | &nbsp; {time_str} WIB
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(1)

    # init timer
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = time.time()

    # refresh tiap 60 detik
    if time.time() - st.session_state.last_refresh > 60:
        st.session_state.last_refresh = time.time()
        # st.experimental_rerun()

    # Helper
    # ======================
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

    def apply_safe_rupiah_axis(fig, series):
        max_val = series.max()
        fig.update_yaxes(
            range=[0, max_val * 1.2 if max_val > 0 else 1],
            tickformat=","
        )
    # ======================
    # Load & Filter Data
    # ======================
    df = load_aset_data()
    df = apply_global_filters(df)

    # KUNCI TAHUN AKTIF (SINKRON DENGAN DATETIME)
    # ======================
    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce").fillna(0)

    # ======================
   # FILTER SPER VALID
    # ======================
    df_sper_valid = df[
        df["nomor_surat"].notna() &
        ~df["nomor_surat"].astype(str).str.strip().isin(
            ["", "-", "Fasilitas proyek", "Digunakan Internal PT PAL"]
        )
    ].copy()

    # NORMALISASI (WAJIB)
    # ======================
    df_sper_valid["penyewa"] = (
        df_sper_valid["penyewa"]
        .fillna("Belum Ada Penyewa")
        .astype(str)
        .str.strip()
    )

    df_sper_valid["jenis_aset"] = (
        df_sper_valid["jenis_aset"]
        .fillna("Tidak Diketahui")
        .astype(str)
        .str.strip()
    )

    # DATA UNTUK SEMUA CHART
    # ======================
    # df_chart = df_filtered.copy()

    # ======================
    # FILTER DATA (DI BAWAH METRIC)
    # ======================
    st.subheader("Filter Data")

    f1, f2, f3 = st.columns(3)

    # ======================
    # 1. FILTER TAHUN
    # ======================
    with f1:
        tahun_selected = st.multiselect(
            "Tahun",
            options=sorted(df_sper_valid["tahun"].dropna().astype(int).unique()),
            default=st.session_state.get("tahun_selected", [])
        )

    # ======================
    # 2. FILTER JENIS ASET
    # ======================
    with f2:
        jenis_selected = st.multiselect(
            "Jenis Aset",
            options=sorted(df_sper_valid["jenis_aset"].dropna().unique()),
            default=st.session_state.get("jenis_selected", [])
        )

    # ======================
    # 3. BUAT DATA SEMENTARA UNTUK OPSI PENYEWA
    # ======================
    df_penyewa_option = df_sper_valid.copy()

    if tahun_selected:
        df_penyewa_option = df_penyewa_option[
            df_penyewa_option["tahun"].isin(tahun_selected)
        ]

    if jenis_selected:
        df_penyewa_option = df_penyewa_option[
            df_penyewa_option["jenis_aset"].isin(jenis_selected)
        ]

    # ======================
    # 4. FILTER PENYEWA (SUDAH TERGANTUNG JENIS ASET)
    # ======================
    with f3:
        penyewa_selected = st.multiselect(
            "Penyewa",
            options=sorted(df_penyewa_option["penyewa"].dropna().unique()),
            default=st.session_state.get("penyewa_selected", [])
        )
        
    # SIMPAN KE SESSION
    st.session_state["tahun_selected"] = tahun_selected
    st.session_state["jenis_selected"] = jenis_selected
    st.session_state["penyewa_selected"] = penyewa_selected
    
    df_filtered = df_sper_valid.copy()

    if tahun_selected:
        df_filtered = df_filtered[df_filtered["tahun"].isin(tahun_selected)]

    if jenis_selected:
        df_filtered = df_filtered[df_filtered["jenis_aset"].isin(jenis_selected)]

    if penyewa_selected:
        df_filtered = df_filtered[df_filtered["penyewa"].isin(penyewa_selected)]

    df_chart = df_filtered.copy()

    # ======================
    # DATA KHUSUS SUMMARY (DIKUNCI KE TAHUN AKTIF)
    # ======================
    current_year = datetime.now().year

    if tahun_selected:
        df_summary = df_filtered.copy()
    else:
        df_summary = df_filtered[df_filtered["tahun"] == current_year].copy()

    if df_summary.empty:
        st.warning("Tidak ada data untuk filter yang dipilih")
        st.stop()

    st.divider()

    # Summary Global
    # ======================
    st.subheader("Summary")
    df_metric = df_summary.copy()
    sper_per_aset = (
        df_metric
        .groupby("jenis_aset")["nomor_surat"]
        .size()
    )

    total_sper = int(sper_per_aset.sum())
    total_nilai = df_metric["nilai"].sum()
    total_jenis_aset = df["jenis_aset"].nunique()

    c1, c2, c3 = st.columns(3)
    c1.metric("Kategori / Jenis Aset", total_jenis_aset)
    c2.metric("Total SPER", total_sper)
    c3.metric("Total Nilai Kontribusi (Rp)", format_rupiah_singkat(total_nilai))

    st.caption(f"Nilai sebenarnya: Rp {total_nilai:,.0f}".replace(",", "."))

    c4, c5, c6, c7, c8 = st.columns(5)
    c4.metric("SPER Rumah Dinas", int(sper_per_aset.get("Rumah Dinas", 0)))
    c5.metric("SPER Kantor", int(sper_per_aset.get("Kantor", 0)))
    c6.metric("SPER Kontainer", int(sper_per_aset.get("Kontainer", 0)))
    c7.metric("SPER Lahan", int(sper_per_aset.get("Lahan", 0)))
    c8.metric("SPER Mess Menanggal", int(sper_per_aset.get("Mess", 0)))
    st.divider()

    render_map()

    # =============================
    # LINE CHART – TREN NILAI KONTRIBUSI (SEMUA TAHUN)
    # =============================
    st.subheader("Tren Nilai Kontribusi SPER per Tahun")
    trend = (
        df_chart
        .groupby("tahun", as_index=False)
        .agg(total_nilai=("nilai", "sum"))
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
        tickformat="d"   # penting: tahun tidak pakai koma
    )
    fig_line.update_yaxes(tickformat=",")
    st.plotly_chart(fig_line, width="stretch")
    st.divider()
    
    # Distribusi & Komposisi
    # ====================== 
    current_year = datetime.now().year

    if tahun_selected:
        df_chart = df_filtered.copy()
    else:
        df_chart = df_filtered[df_filtered["tahun"] == current_year].copy()  

    st.header("Proporsi Aset dan Nilai Kontribusi")
    c9, c10  = st.columns(2)
    with c9:
        df_jenis_count = (
            df_chart
            .groupby("jenis_aset", as_index=False)
            .size()
            .rename(columns={"size": "jumlah_sper"})
        )
        urutan_aset = [
            "Rumah Dinas",
            "Kantor",
            "Kontainer",
            "Lahan",
            "Mess"
        ]
        df_jenis_count["jenis_aset"] = pd.Categorical(
            df_jenis_count["jenis_aset"],
            categories=urutan_aset,
            ordered=True
        )

        df_jenis_count = df_jenis_count.sort_values("jenis_aset")

        total_sper = df_jenis_count["jumlah_sper"].sum()
        df_jenis_count["persentase"] = (
            df_jenis_count["jumlah_sper"] / total_sper * 100
        ).round(1)

        fig_pie = px.pie(
            df_jenis_count,
            names="jenis_aset",
            values="jumlah_sper",   # tetap dipakai untuk proporsi
            hole=0.4,
            title="Proporsi SPER per Jenis Aset",
            category_orders={"jenis_aset": urutan_aset}
        )
        fig_pie.update_traces(
            textinfo="percent+label",
            hovertemplate=
                "<b>Jenis Aset</b>: %{label}<br>" +
                "<b>Jumlah</b>: %{value}<extra></extra>"
        )

        st.plotly_chart(fig_pie, width="stretch")
    with c10:
        df_jenis_nilai = (
            df_chart
            .groupby("jenis_aset", as_index=False)["nilai"]
            .sum()
        )
        urutan_aset = [
            "Rumah Dinas",
            "Kantor",
            "Kontainer",
            "Lahan",
            "Mess"
        ]
        df_jenis_nilai["jenis_aset"] = pd.Categorical(
            df_jenis_nilai["jenis_aset"],
            categories=urutan_aset,
            ordered=True
        )
        df_jenis_nilai = df_jenis_nilai.sort_values("jenis_aset")
        fig_pie_nilai = px.pie(
            df_jenis_nilai,
            names="jenis_aset",
            values="nilai",
            hole=0.4,
            title=f"Proporsi Nilai Kontribusi Aset"
        )
        fig_pie_nilai.update_traces(
            textinfo="percent+label",
            hovertemplate=
                "<b>Jenis Aset</b>: %{label}<br>" +
                "<b>Nilai</b>: Rp %{value:,.0f}<extra></extra>"
        )
        st.plotly_chart(fig_pie_nilai, width="stretch")
    
    # ============================
    st.subheader("Distribusi Aset")
    
    df_jenis = (
        df_chart
        .groupby("jenis_aset", as_index=False)["nilai"]
        .sum()
        .sort_values("nilai")
    )
    urutan_aset = [
        "Rumah Dinas",
        "Kantor",
        "Kontainer",
        "Lahan",
        "Mess"
    ]

    df_jenis["jenis_aset"] = pd.Categorical(
        df_jenis["jenis_aset"],
        categories=urutan_aset,
        ordered=True
    )

    df_jenis = df_jenis.sort_values("jenis_aset")

    df_jenis["label_nilai"] = df_jenis["nilai"].apply(label_nilai_id)
    df_jenis["tooltip_nilai"] = df_jenis["nilai"].apply(format_rupiah_full)

    fig_bar = px.bar(
        df_jenis,
        x="jenis_aset",
        y="nilai",
        color="jenis_aset",
        labels={
            "jenis_aset": "Jenis Aset",
            "nilai": "Nilai Kontribusi"
        },
        title="Total Kontribusi per Jenis Aset"
    )
    fig_bar.update_traces(
        texttemplate="Rp %{y:,.0f}",     
        textposition="outside",
        hovertemplate=
            "<b>Aset</b>: %{x}<br>" +
            "<b>Total Nilai</b>: Rp %{y:,.0f}<extra></extra>"
    )
    fig_bar.update_xaxes(categoryorder="array", categoryarray=urutan_aset)
    apply_safe_rupiah_axis(fig_bar, df_jenis["nilai"])
    
    fig_bar.update_layout(height=500)
    st.plotly_chart(fig_bar, width="stretch")

    # Tren & Ranking
    # =======================
    st.subheader("Top 10 Penyewa Berdasarkan Nilai Kontribusi")
    #========================
    # Top Penyewa
    
    if "penyewa" in df_sper_valid.columns:
        df_top = (
            df_chart
            .groupby("penyewa")
            .agg(
                nilai=("nilai", "sum"),
                aset=("jenis_aset", lambda x: ", ".join(sorted(x.unique())))
            )
            .reset_index()
            .sort_values("nilai", ascending=False)
            .head(10)
        )

        df_top["label_nilai"] = df_top["nilai"].apply(label_nilai_id)
        df_top["tooltip_nilai"] = df_top["nilai"].apply(format_rupiah_full)

        fig_hbar = px.bar(
            df_top,
            x="nilai",
            y="penyewa",
            orientation="h",
            text="label_nilai",
            labels={
                "nilai": "Nilai Kontribusi",
                "penyewa": "Penyewa"
            }
        )
        fig_hbar.update_traces(
            textposition="outside",
            cliponaxis=False, 
            hovertemplate=
                "<b>Penyewa</b>: %{y}<br>"
                "<b>Total Nilai</b>: %{customdata[0]}<br>"
                "<b>Jenis Aset</b>: %{customdata[1]}"
                "<extra></extra>",
            customdata=df_top[["tooltip_nilai", "aset"]].values
        )
        fig_hbar.update_xaxes(tickformat=",")
        fig_hbar.update_yaxes(categoryorder="total ascending")
        fig_hbar.update_layout(height=500)

        st.plotly_chart(fig_hbar, width="stretch")

    else:
        st.warning("Kolom 'penyewa' tidak ditemukan")

    st.divider()


    # =======================================

    def normalize_status(text):
        if pd.isna(text):
            return "Tidak Diketahui"

        text = str(text).strip().lower()

        mapping = {
            # umum
            "disewa": "Disewa",
            "kosong": "Kosong",
            "digunakan internal": "Digunakan Internal",
            "digunakan internal pal": "Digunakan Internal",

            # kondisi
            "baik": "Kondisi Baik",
            "kondisi baik": "Kondisi Baik",
            "rusak": "Rusak",
            "rusak ringan": "Rusak",
            "rusak berat": "Rusak Berat",
            "butuh perbaikan": "Butuh Perbaikan",

            # operasional
            "proses": "Proses",
            "fasilitas proyek": "Fasilitas Proyek"
        }

        return mapping.get(text, text.title())

    # ============================
    # STATUS ASET PER JENIS ASET (LENGKAP ENUM)
    # ============================
    st.subheader("Status Aset per Jenis Aset")

    urutan_aset = [
        "Rumah Dinas",
        "Kantor",
        "Kontainer",
        "Lahan",
        "Mess"
    ]

    urutan_status = [
        "Kosong",
        "Disewa",
        "Internal",
        "Perbaikan",
        "Tidak Aktif"
    ]

    df_status_raw = df.copy()

    # 🔥 FIX UTAMA: aset fisik harus unik
    df_status_raw = df_status_raw.drop_duplicates(subset=["kode_aset"])

    # Filter hanya berdasarkan jenis aset
    if jenis_selected:
        df_status_raw = df_status_raw[
            df_status_raw["jenis_aset"].isin(jenis_selected)
        ]

    df_status_raw["status_aset"] = (
        df_status_raw["status_aset"]
        .apply(normalize_status)
    )

    summary = (
        df_status_raw
        .groupby(["jenis_aset", "status_aset"])
        .size()
        .reset_index(name="jumlah")
    )

    # ===============================
    # PAKSA SEMUA KOMBINASI MUNCUL
    # ===============================
    all_jenis = df_status_raw["jenis_aset"].unique()
    all_status = ["Kosong", "Disewa", "Internal", "Tidak Aktif", "Perbaikan"]
    
    index_full = pd.MultiIndex.from_product(
        [all_jenis, all_status],
        names=["jenis_aset", "status_aset"]
    )

    summary = (
        summary
        .set_index(["jenis_aset", "status_aset"])
        .reindex(index_full, fill_value=0)
        .reset_index()
    )

    summary["jenis_aset"] = pd.Categorical(
        summary["jenis_aset"],
        categories=urutan_aset,
        ordered=True
    )

    summary["status_aset"] = pd.Categorical(
        summary["status_aset"],
        categories=urutan_status,
        ordered=True
    )

    # ============================
    # CHART
    # ============================
    fig_status = px.bar(
        summary,
        x="jenis_aset",
        y="jumlah",
        color="status_aset",
        text="jumlah",
        labels={
            "status_aset": "Status Aset",
            "jenis_aset": "Jenis Aset",
            "jumlah": "Jumlah"
        },
        category_orders={
            "jenis_aset": urutan_aset,
            "status_aset": [
                "Kosong",
                "Disewa",
                "Internal",
                "Tidak Aktif",
                "Perbaikan"
            ]
        }
    )

    fig_status.update_traces(
        textposition="inside",
        hovertemplate=
            "<b>Jenis Aset</b>: %{x}<br>"
            "<b>Status</b>: %{fullData.name}<br>"
            "<b>Jumlah</b>: %{y}<extra></extra>"
    )
    fig_status.update_layout(
        barmode="stack",
        height=560,
        legend_title_text="Status Aset"
    )

    fig_status.update_xaxes(
        categoryorder="array",
        categoryarray=urutan_aset
    )

    st.plotly_chart(fig_status, width="stretch")
