import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_aset_data
from data_loader import load_master_penghapusbukuan_aset
from filters import apply_global_filters
from datetime import datetime
import time
import folium 
from streamlit_folium import st_folium
from maps.leaflet_maps import render_map
from maps.leaflet_maps_areaPAL import render_map_area_PAL


def show_Dashboard_Global():
    st.title("🔔 Dashboard Global Aset")

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

    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = time.time()

    if time.time() - st.session_state.last_refresh > 60:
        st.session_state.last_refresh = time.time()
        
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

    # def warna_progres(val):
    #     val = str(val).strip().lower()

    #     if val == "belum" :
    #         return "background-color:#FF0900; color:white; text-align:center; font-weight:bold;"
    #     elif val == "proses" :
    #         return "background-color:#FFCA09; color:white; text-align:center; font-weight:bold;"
    #     elif val == "selesai" :
    #         return "background-color:#12D200; color:white; text-align:center; font-weight:bold;"
    #     else :
    #         return ""

    # ======================
    df = load_aset_data()
    df = apply_global_filters(df)

    # ======================
    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce").fillna(0)

    # ======================
    df_sper_valid = df[
        df["nomor_surat"].notna() &
        ~df["nomor_surat"].astype(str).str.strip().isin(
            ["", "-", "Fasilitas proyek", "Digunakan Internal PT PAL"]
        )
    ].copy()

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

    # ======================
    # df_chart = df_filtered.copy()
    st.subheader("Filter Data")
    f1, f2, f3 = st.columns(3)

    # =================
    df_base = df_sper_valid.copy()

    # =================
    with f1:
        tahun_selected = st.multiselect(
            "Tahun",
            options=sorted(df_base["tahun"].dropna().astype(int).unique()),
            default=st.session_state.get("tahun_selected", [])
        )

    if tahun_selected:
        df_base = df_base[df_base["tahun"].isin(tahun_selected)]

    # ==================
    with f2:
        jenis_selected = st.multiselect(
            "Jenis Aset",
            options=sorted(df_base["jenis_aset"].dropna().unique()),
            default=st.session_state.get("jenis_selected", [])
        )

    if jenis_selected:
        df_base = df_base[df_base["jenis_aset"].isin(jenis_selected)]

    # ===================
    with f3:
        penyewa_selected = st.multiselect(
            "Penyewa",
            options=sorted(df_base["penyewa"].dropna().unique()),
            default=st.session_state.get("penyewa_selected", [])
        )

    # ===================
    st.session_state["tahun_selected"] = tahun_selected
    st.session_state["jenis_selected"] = jenis_selected
    st.session_state["penyewa_selected"] = penyewa_selected

    # ===================
    df_filtered = df_sper_valid.copy()

    if tahun_selected:
        df_filtered = df_filtered[df_filtered["tahun"].isin(tahun_selected)]

    if jenis_selected:
        df_filtered = df_filtered[df_filtered["jenis_aset"].isin(jenis_selected)]

    if penyewa_selected:
        df_filtered = df_filtered[df_filtered["penyewa"].isin(penyewa_selected)]

    df_chart = df_filtered.copy()

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

    # ==========================
    st.subheader("Summary")
    df_metric = df_summary.copy()
    sper_per_aset = (
        df_metric
        .groupby("jenis_aset")["kode_aset"]
        .nunique()
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
    
    # =======================
    if 'map_mode' not in st.session_state:
        st.session_state.map_mode = "pendayagunaan aset"

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Peta Pendayagunaan Aset",
            use_container_width=True
        ):
            st.session_state.map_mode = "pendayagunaan aset"

    with col2:
        if st.button(
            "Peta Penghapusbukuan Aset",
            use_container_width=True
        ):
            st.session_state.map_mode = "penghapusan aset"

    # st.subheader("Peta Sebaran Aset dengan SPER")
    if st.session_state.map_mode == "pendayagunaan aset":
        render_map()
        
    elif st.session_state.map_mode == "penghapusan aset":
        render_map_area_PAL()
    
    st.info(f"Mode Peta Aktif : **{st.session_state.map_mode.capitalize()}**")
    st.divider()
    # =======================
    st.subheader("📋 Detail Data Penghapusbukuan Aset")
    df_penghapusbukuan_aset = load_master_penghapusbukuan_aset()
    df_penghapusbukuan = df_penghapusbukuan_aset[[
        "nama_aset", "ppa", "penerbitan_lhpb", "kajian_manrisk_legal",
        "review_div_otb", "approval_im4_kajian_penghapusbukuan",
        "verbal_surat_dirut", "rekom_persetujuan_komisaris",
        "persetujuan_fidusia", "persetujuan_rups",
        "skep_penghapusbukuan", "penjualan_pemindahtanganan_aset", "keterangan"
    ]].rename(columns={
        "nama_aset": "Nama Aset",
        "ppa": "PPA (Permohonan Penghapusan Aset)",
        "penerbitan_lhpb": "Penerbitan LHPB",
        "kajian_manrisk_legal": "Kajian Manajemen Risiko dan Legal",
        "review_div_otb": "Review Divisi Office Of The Board",
        "approval_im4_kajian_penghapusbukuan": "Approval IM4 Kajian Penghapusbukuan",
        "verbal_surat_dirut": "Verbal Surat Direktur Utama kepada Dewan Komisaris",
        "rekom_persetujuan_komisaris": "Rekomendasi / Persetujuan Dewan Komisaris",
        "persetujuan_fidusia": "Persetujuan Fidusia (Optional)",
        "persetujuan_rups": "Persetujuan RUPS",
        "skep_penghapusbukuan": "SKEP Penghapusbukuan Aset",
        "penjualan_pemindahtanganan_aset": "Penjualan / Pemindahtanganan Aset",
        "keterangan": "Keterangan"
    })

    st.markdown("""
    <style>
        /* 1. Atur container utama agar selaras dengan konten lain */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 3rem; /* Memberikan jarak tepi kiri */
            padding-right: 3rem; /* Memberikan jarak tepi kanan */
            max-width: 100% !important;
            padding: 1.5rem !important;
            max-width: 100% !important;
        }

        /* 2. Pembungkus Tabel dengan batas lebar maksimal agar tidak meluap */
        .table-container {
            width: 100%;
            max-width: 1200px; /* Sesuaikan dengan lebar rata-rata chart Anda */
            margin: 0 auto; /* Menengahkan tabel */
            overflow-x: auto; /* Scrollbar horizontal muncul hanya jika diperlukan */
            border: 1px solid #e6e9ef;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            background-color: white;
            padding: 10px;
        }
        
        /* 3. Gaya Tabel Custom */
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            font-size: clamp(6px, 0.7vw, 11px);
            font-family: 'Inter', sans-serif;
            table-layout: fixed; /* Kolom menyesuaikan isi secara cerdas */
        }
        
        .custom-table th {
            background-color: #f8f9fa;
            color: #31333F;
            font-weight: 600;
            text-align: center !important;
            vertical-align: middle !important;
            padding: 12px 8px !important;
            border-bottom: 2px solid #dee2e6;
            white-space: normal !important; /* Wrap text untuk judul kolom yang panjang */
            line-height: 1.2;
        }

        .custom-table td {
            padding: 4px 3px;
            border-bottom: 1px solid #f0f2f6;
            vertical-align: middle;
            text-align: center;
        }

        /* Kolom Nama Aset dibuat lebih lebar dan rata kiri */
        .custom-table td:nth-child(2) {
            text-align: left !important;
            min-width: 100px;
            font-weight: 600;
        }

        /* Gaya Badge Status agar lebih kecil dan rapi */
        .badge-status {
            display: inline-block;
            padding: 2px 0px;
            width: 30px; /* Lebar tetap agar seragam */
            border-radius: 4px;
            color: black;
            font-weight: bold;
            font-size: 15px;
            text-align: center;
        }
        .badge-status-selesai {
            display: inline-block;
            padding: 2px 0px;
            width: 30px; /* Lebar tetap agar seragam */
            border-radius: 4px;
            color: white;
            font-weight: bold;
            font-size: 15px;
            text-align: center;
        }
        .bg-selesai { background-color: #12D200; }
        .bg-proses { background-color: #FFCA09; }
        .bg-belum { background-color: #FF0900; }
    </style>
    """, unsafe_allow_html=True)

    def make_pretty(val):
        v = str(val).strip().lower()
        if v == 'selesai': return f'<div class="badge-status-selesai bg-selesai">✔</div>'
        if v == 'proses': return f'<div class="badge-status bg-proses">🛠</div>'
        if v == 'belum': return f'<div class="badge-status bg-belum">⏳</div>'
        return val if not pd.isna(val) and val != "None" else ""
    

    kolom_status = df_penghapusbukuan.columns[1:-1] 
    df_html = df_penghapusbukuan.copy()
    for col in kolom_status:
        df_html[col] = df_html[col].apply(make_pretty)

    df_html.index = range(1, len(df_html) + 1)
    df_html = df_html.reset_index().rename(columns={'index': 'No'})
    
    html_string = df_html.to_html(escape=False, index=False, classes='custom-table')
    st.markdown(f'<div class="table-wrapper">{html_string}</div>', unsafe_allow_html=True)
    
    st.divider()

    # =======================
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
        tickformat="d"
    )
    fig_line.update_yaxes(tickformat=",")
    st.plotly_chart(fig_line, width="stretch")
    st.divider()
    
    # Distribusi & Komposisi 
    current_year = datetime.now().year

    if tahun_selected:
        df_chart = df_filtered.copy()
    else:
        df_chart = df_filtered[df_filtered["tahun"] == current_year].copy()  

    st.header("Proporsi Aset dan Nilai Kontribusi")
    c9, c10  = st.columns([1.8,1])
    with c9:
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
        
        fig_bar.update_layout(height=550)
        st.plotly_chart(fig_bar, width="stretch")
        
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
        fig_pie_nilai.update_layout(height=550)
        st.plotly_chart(fig_pie_nilai, width="stretch")

    st.divider()

    # =======================
    st.subheader("Penyewa Berdasarkan Nilai Kontribusi")

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
            "internal": "Internal",
            "digunakan internal": "Internal",
            "digunakan internal pal": "Internal",
            
            # kondisi
            "baik": "Kondisi Baik",
            "kondisi baik": "Kondisi Baik",
            "rusak": "Rusak",
            "rusak ringan": "Rusak",
            "rusak berat": "Rusak Berat",
            "butuh perbaikan": "Butuh Perbaikan",
            "perbaikan": "Perbaikan",
            "tidak aktif": "Tidak Aktif",
            "fasilitas proyek": "Internal",

            # operasional
            "proses": "Proses",
            "fasilitas proyek": "Fasilitas Proyek"
        }

        return mapping.get(text, text.title())

    # ============================
    st.subheader("Distribusi Kondisi Aset")

    from data_loader import (
        load_master_rumdin,
        load_master_kantor,
        load_master_kontainer,
        load_master_lahan,
        load_master_mess
    )

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
        "Tidak Aktif",
        "Perbaikan"
    ]

    df_rumdin = load_master_rumdin()
    df_rumdin["jenis_aset"] = "Rumah Dinas"
    df_rumdin = df_rumdin.rename(columns={"kode_rumdin": "kode_aset"})

    df_kantor = load_master_kantor()
    df_kantor["jenis_aset"] = "Kantor"
    df_kantor = df_kantor.rename(columns={"kode_kantor": "kode_aset"})

    df_kontainer = load_master_kontainer()
    df_kontainer["jenis_aset"] = "Kontainer"
    df_kontainer = df_kontainer.rename(columns={"kode_kontainer": "kode_aset"})

    df_lahan = load_master_lahan()
    df_lahan["jenis_aset"] = "Lahan"
    df_lahan = df_lahan.rename(columns={"kode_lahan": "kode_aset"})

    df_mess = load_master_mess()
    df_mess["jenis_aset"] = "Mess"
    df_mess = df_mess.rename(columns={"kode_mess": "kode_aset"})

    df_master = pd.concat(
        [df_rumdin, df_kantor, df_kontainer, df_lahan, df_mess],
        ignore_index=True
    )

    df_master["status_aset"] = df_master["status_aset"].apply(normalize_status)

    if jenis_selected:
        df_master = df_master[df_master["jenis_aset"].isin(jenis_selected)]

    summary = (
        df_master
        .groupby(["jenis_aset", "status_aset"])
        .size()
        .reset_index(name="jumlah")
    )

    index_full = pd.MultiIndex.from_product(
        [urutan_aset, urutan_status],
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

    summary = summary.sort_values(["jenis_aset", "status_aset"])

    # ===========================
    c11,c12 = st.columns([1,1.3])
    with c11:
        df_jenis_count = (
            df_chart
            .drop_duplicates(subset=["kode_aset"])
            .groupby("jenis_aset", as_index=False)["kode_aset"]
            .nunique()
            .rename(columns={"kode_aset": "jumlah_sper"})
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
            values="jumlah_sper",
            hole=0.4,
            title="Proporsi SPER Terhadap Jenis Aset",
            category_orders={"jenis_aset": urutan_aset}
        )
        fig_pie.update_traces(
            textinfo="percent+label",
            hovertemplate=
                "<b>Jenis Aset</b>: %{label}<br>" +
                "<b>Jumlah</b>: %{value}<extra></extra>"
        )
        fig_pie.update_layout(height=620)
        st.plotly_chart(fig_pie, width="stretch")

    with c12:
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
                "status_aset": urutan_status
            },
            title="Distribusi Kondisi Aset"
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
            height=620,
            legend_title_text="Status Aset"
        )

        fig_status.update_xaxes(
            categoryorder="array",
            categoryarray=urutan_aset
        )

        st.plotly_chart(fig_status, width="stretch")
