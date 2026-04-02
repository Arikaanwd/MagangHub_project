import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_aset_data, load_master_mess
from datetime import datetime
import time
from database import fetch


@st.cache_data
def load_mess_data():
    query = """
    SELECT 
        mm.kode_mess AS kode_aset,
        mm.status_aset,
        mm.blok AS keterangan,
        tm.id_transaksi,
        tm.penyewa,
        tm.unit_kerja AS lokasi,
        tm.nomor_surat,
        tm.tanggal_mulai,
        tm.tanggal_selesai,
        tm.durasi_bulan,
        tm.nilai_kontribusi_perbulan
    FROM master_mess mm
    LEFT JOIN transaksi_mess tm ON mm.id_mess = tm.id_mess
    
    """
    data, columns = fetch(query)
    df = pd.DataFrame(data, columns=columns)

    df["tanggal_mulai"] = pd.to_datetime(df["tanggal_mulai"], errors="coerce")
    df["tanggal_selesai"] = pd.to_datetime(df["tanggal_selesai"], errors="coerce")
    df["nilai_kontribusi_perbulan"] = pd.to_numeric(df["nilai_kontribusi_perbulan"], errors="coerce").fillna(0)

    return df

# =====================
def hitung_revenue_tahun(row, tahun):
    if pd.isna(row["tanggal_mulai"]) or pd.isna(row["tanggal_selesai"]):
        return 0

    start = max(row["tanggal_mulai"], pd.Timestamp(f"{tahun}-01-01"))
    end = min(row["tanggal_selesai"], pd.Timestamp(f"{tahun}-12-31"))

    if start > end:
        return 0

    bulan = (end.year - start.year) * 12 + (end.month - start.month) + 1
    return bulan * row["nilai_kontribusi_perbulan"]

def show_Mess_Menanggal():
    st.title("🏨Dashboard SPER Mess Menanggal")

    # st.title("🏨Dashboard SPER Mess Menanggal")
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
    df = load_mess_data()
    df_master_mess = load_master_mess()
    df_tahun = df.copy()
    tahun_list = sorted(
        set(df_tahun["tanggal_mulai"].dt.year.dropna().astype(int)) |
        set(df_tahun["tanggal_selesai"].dt.year.dropna().astype(int))
    )
    df_all_mess = df.copy()

    #============================
    df_all_mess = load_aset_data()
    df_all_mess = df_all_mess[df_all_mess["jenis_aset"] == "Mess"].copy()
    
    #=====================
    # df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce").fillna(0)
    # df["nilai_perbulan"] = pd.to_numeric(df["nilai_perbulan"], errors="coerce").fillna(0)
    df["durasi_bulan"] = pd.to_numeric(df["durasi_bulan"], errors="coerce").fillna(0)
    
    # ==========================
    st.header("Filter Mess Menanggal")
    j1, j2, j3, j4 = st.columns(4)
    df_base = df.copy()
    
    with j1:
        tahun_list = sorted(
            set(df["tanggal_mulai"].dt.year.dropna().astype(int)) |
            set(df["tanggal_selesai"].dt.year.dropna().astype(int))
        )
        tahun = st.multiselect("Tahun SPER", tahun_list)

        if tahun:
            df_base = df_base[
                (df_base["tanggal_mulai"].dt.year.isin(tahun)) |
                (df_base["tanggal_selesai"].dt.year.isin(tahun))
            ]
        
    with j2:
        penyewa_list = sorted(df_base["penyewa"].dropna().unique())
        penyewa = st.multiselect("Penyewa", penyewa_list)

        if penyewa:
            df_base = df_base[df_base["penyewa"].isin(penyewa)]

    with j3:
        status_list = sorted(df_base["status_aset"].dropna().unique())
        status_selected = st.multiselect("Status", status_list)

        if status_selected:
            df_base = df_base[df_base["status_aset"].isin(status_selected)]

    lantai_mapping = {
        "1": [c for c in "A B C D E F G H".split()] + ["AA","BB","CC","DD","EE","FF","GG","HH"],
        "2": [f"{c}1" for c in "A B C D E F G H".split()] + ["AA1","BB1","CC1","DD1","EE1","FF1","GG1","HH1"],
        "3": [f"{c}2" for c in "A B C D E F G H".split()] + ["AA2","BB2","CC2","DD2","EE2","FF2","GG2","HH2"],
        "4": [f"{c}3" for c in "A B C D E F G H".split()] + ["AA3","BB3","CC3","DD3","EE3","FF3","GG3","HH3"]
    }

    def get_lantai(kamar):
        for lantai, kamar_list in lantai_mapping.items():
            if kamar in kamar_list:
                return lantai
        return "Tidak Diketahui"

    df_base["lantai"] = df_base["keterangan"].astype(str).apply(get_lantai)

    with j4:
        lantai_list = sorted(df_base["lantai"].unique())
        lantai_selected = st.multiselect("Lantai", lantai_list)

        if lantai_selected:
            df_base = df_base[df_base["lantai"].isin(lantai_selected)]

    # =========================
    df_filtered = df_base.copy()
    
    #=====================
    # df_sper_valid = df[
    #     df["nomor_surat"].notna() &
    #     (df["nomor_surat"].str.strip() != " ") &
    #     (df["nomor_surat"].str.strip() != "") &
    #     (df["nomor_surat"].str.strip() != "-")     
    # ].copy()

    # ==========================
    tahun_dashboard = tahun[0] if tahun else datetime.now().year
    df_filtered["revenue_tahun"] = df_filtered.apply(
        lambda r: hitung_revenue_tahun(r, tahun_dashboard), axis=1
    )
    df_filtered = df_filtered[df_filtered["revenue_tahun"] > 0].copy()

    # if selected_year and len(selected_year) > 0:
    #     df_chart = df_sper_valid[df_sper_valid["tahun"].isin(selected_year)].copy()
    # else:
    #     # default: tahun saat ini
    #     df_chart = df_sper_valid[df_sper_valid["tahun"] == current_year].copy()

    if df_filtered.empty:
        st.warning("Tidak ada data SPER untuk tahun yang dipilih")
        st.stop()
    
    df_sper_valid = df_filtered[
        df_filtered["nomor_surat"].notna() &
        (df_filtered["nomor_surat"].str.strip() != "") &
        (df_filtered["nomor_surat"].str.strip() != "-")
    ].copy()

    #=====================
    total_sper = df_filtered["kode_aset"].nunique()
    total_nilai = df_filtered["revenue_tahun"].sum()
    total_mess = df_master_mess["kode_mess"].nunique()
    rata_nilai = df_filtered["revenue_tahun"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total SPER", total_sper)
    c2.metric("Total Kamar", total_mess)
    c3.metric("Total Nilai Kontribusi (Rp)", format_rupiah_singkat(total_nilai))
    c4.metric("Rata-rata Nilai per Mess", format_rupiah_singkat(rata_nilai))
    st.caption(f"Nilai sebenarnya: {format_rupiah_full(total_nilai)}")

    st.divider()    
    
    # ==================
    st.subheader("Tren Nilai Kontribusi SPER per Tahun")
    if df["tanggal_mulai"].notna().any():
        start_year = int(df["tanggal_mulai"].dt.year.dropna().min())
    else:
        start_year = datetime.now().year

    current_year = datetime.now().year
    years = list(range(start_year, current_year + 1))
    trend_list = []

    for y in years:
        temp = df.copy()
        temp["rev"] = temp.apply(lambda r: hitung_revenue_tahun(r, y), axis=1)
        trend_list.append({"tahun": y, "total_nilai": temp["rev"].sum()})

    trend = pd.DataFrame(trend_list)

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
    top_penyewa=(
        df_filtered
        .groupby("penyewa")["revenue_tahun"]
        .sum()
        .reset_index()
        .sort_values("revenue_tahun", ascending=True)
        .head(10)
    )
    top_penyewa["label_nilai"] = top_penyewa["revenue_tahun"].apply(label_nilai_id)
    top_penyewa["tooltip_nilai"] = top_penyewa["revenue_tahun"].apply(format_rupiah_full)
    
    # fig_penyewa = px.bar(
    #     top_penyewa,
    #     x="nilai",
    #     y="penyewa",
    #     orientation="h",
    #     text="label_nilai",
    #     labels={
    #         "nilai": "Nilai Kontribusi (Rp)",
    #         "penyewa": "Penyewa"
    #     }
    # )
    # fig_penyewa.update_traces(
    #     textposition="outside",
    #     hovertemplate=
    #         "<b>Penyewa</b>: %{y}<br>" +
    #         "<b>Nilai Kontribusi</b>: %{customdata}<extra></extra>",
    #     customdata=top_penyewa["tooltip_nilai"]
    # )
    # fig_penyewa.update_xaxes(
    #     tickformat=","
    # )
    # fig_penyewa.update_layout(height=480)
    # st.plotly_chart(fig_penyewa, width="stretch")
    # barchart lantai

    # ================
    st.subheader("Distribusi SPER per Lantai Mess Menanggal")
    df_filtered["lantai"] = df_filtered["keterangan"].astype(str).apply(get_lantai)
    
    df_lantai = df_filtered[
        (df_filtered["nomor_surat"].notna()) &
        (df_filtered["nomor_surat"].str.strip() != "")
    ].copy()

    df_lantai["revenue_tahun"] = df_lantai.apply(lambda r: hitung_revenue_tahun(r, tahun_dashboard), axis=1)
    df_lantai = df_lantai[df_lantai["revenue_tahun"] > 0]

    lantai_dist = (
        df_lantai
        .groupby("lantai", as_index=False)
        .agg(
            total_nilai=("revenue_tahun", "sum"),
            jumlah_sper=("nomor_surat", "nunique")
        )
        .sort_values("lantai", ascending=False)
    )

    top_penyewa["label_nilai"] = top_penyewa["revenue_tahun"].apply(label_nilai_id)
    top_penyewa["tooltip_nilai"] = top_penyewa["revenue_tahun"].apply(format_rupiah_full)
    
    fig_lantai = px.bar(
        lantai_dist,
        x="lantai",
        y="total_nilai",
        labels={
            "lantai": "Lantai",
            "total_nilai": "Nilai Kontribusi (Rp)"
        },
        custom_data=["jumlah_sper"]
    )
    fig_lantai.update_traces(
        texttemplate="Rp %{y:,.0f}",     
        textposition="outside",
        hovertemplate=
            "<b>Lantai</b>: %{x}<br>"
            "<b>Jumlah SPER</b>: %{customdata[0]}<br>"
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
    
    # =================================
    st.subheader("Distribusi SPER Terhadap Lokasi Unit Kerja Penyewa dan Proporsi Kondisi Aset")
    
    unit_kerja = (
        df_filtered
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
    
    # ==============================
    df_status = df_master_mess.copy()
    # start_year = pd.Timestamp(f"{tahun_dashboard}-01-01")
    # end_year = pd.Timestamp(f"{tahun_dashboard}-12-31")
    
    # df_sewa_tahun = df[
    #     (df["tanggal_mulai"] <= end_year) &
    #     (df["tanggal_selesai"] >= start_year)
    # ].copy()

    df_sewa_tahun = df_filtered.copy()

    if penyewa:
        df_sewa_tahun = df_sewa_tahun[df_sewa_tahun["penyewa"].isin(penyewa)]

    if lantai_selected:
        df_sewa_tahun["lantai"] = df_sewa_tahun["keterangan"].astype(str).apply(get_lantai)
        df_sewa_tahun = df_sewa_tahun[df_sewa_tahun["lantai"].isin(lantai_selected)]

    kamar_disewa = df_sewa_tahun["kode_aset"].unique()
    df_status["status_tahun"] = df_status["kode_mess"].apply(
        lambda x: "Disewa" if x in kamar_disewa else df_status.loc[df_status["kode_mess"] == x, "status_aset"].values[0]
    )
    status_count = (
        df_status
        .groupby("status_tahun")
        .size()
        .reset_index(name="Jumlah")
    )
    fig_status = px.pie(
        status_count,
        names="status_tahun",
        values="Jumlah",
        title=f"Proporsi Kondisi Aset Mess Tahun {tahun_dashboard}"
    )
    fig_status.update_traces(
        textinfo="percent+label",
        hovertemplate="Status Aset: %{label}<br>Jumlah: %{value}<extra></extra>"
    )
    fig_status.update_layout(height=550)

    c5, c6 = st.columns([1.8,1])
    with c5:
        st.plotly_chart(fig_bar, width="stretch")
    with c6:
        st.plotly_chart(fig_status, width="stretch")
        
    st.divider()
    
    # ==================================
    df_filtered = df_filtered.reset_index(drop=True)
    df_filtered.index = df_filtered.index + 1
    df_filtered["nilai_rupiah"] = df_filtered["revenue_tahun"].apply(format_rupiah)

    st.subheader("📋Detail SPER Mess Menanggal")
    df_filtered["tanggal_mulai_tgl"] = df_filtered["tanggal_mulai"].apply(format_tanggal_indo)
    df_filtered["tanggal_selesai_tgl"] = df_filtered["tanggal_selesai"].apply(format_tanggal_indo)
    st.dataframe(
        df_filtered[[
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
            "nilai_rupiah": "Nilai Kontribusi Pertahun (Rp)",
            "tanggal_mulai_tgl": "Tanggal Mulai",
            "tanggal_selesai_tgl": "Tanggal Selesai",
            "status_aset": "Status"
        }),
        width="stretch"
    )


