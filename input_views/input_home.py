import streamlit as st
import pandas as pd
from data_loader import load_aset_data
from datetime import datetime

def format_tanggal_angka(val):
    if val is None or pd.isna(val):
        return ""
    return val.strftime("%d-%m-%Y")

def format_rupiah(value):
    try:
        value = float(value)
        return f"Rp {value:,.0f}".replace(",", ".")
    except:
        return "Rp 0"

def hitung_status_aset(row):
    today = datetime.today().date()

    status_raw = str(row.get("status_aset", "")).lower()
    nomor_surat = row.get("nomor_surat")
    tgl_selesai = row.get("tanggal_selesai")

    # ================= ASET INTERNAL / PERBAIKAN =================
    if status_raw in ["internal", "perbaikan"]:
        return status_raw.capitalize()

    # ================= TIDAK ADA TRANSAKSI =================
    if pd.isna(nomor_surat) or nomor_surat == "-":
        return "Kosong"

    # ================= TRANSAKSI TANPA TANGGAL =================
    if pd.isna(tgl_selesai):
        return "Disewa"

    # ================= TRANSAKSI SELESAI =================
    if tgl_selesai.date() < today:
        return "Selesai"

    return "Disewa"



ASET_COLUMNS = {
    "Kantor": {
        "nomor_surat": "No. Surat",
        "kode_aset": "Kode Aset",
        "lokasi": "Lokasi",
        "penyewa": "Penyewa",
        "luas_m2": "Luas (m²)",
        "durasi_bulan": "Durasi (Bulan)",
        "tanggal_mulai": "Tanggal Mulai",
        "tanggal_selesai": "Tanggal Selesai",
        "nilai": "Nilai Kontribusi (Rp)",
        "status_aset": "Status Aset"
    },
    "Kontainer": {
        "nomor_surat": "No. Surat",
        "kode_aset": "Kode Aset",
        "lokasi": "Lokasi",
        "penyewa": "Penyewa",
        "volume_feet": "Volume (Feet)",
        "durasi_bulan": "Durasi (Bulan)",
        "tanggal_mulai": "Tanggal Mulai",
        "tanggal_selesai": "Tanggal Selesai",
        "nilai": "Nilai Kontribusi (Rp)",
        "status_aset": "Status Aset"
    },
    "Lahan": {
        "nomor_surat": "No. Surat",
        "kode_aset": "Kode Aset",
        "lokasi": "Lokasi",
        "penyewa": "Penyewa",
        "luas_m2": "Luas (m²)",
        "durasi_bulan": "Durasi (Bulan)",
        "tanggal_mulai": "Tanggal Mulai",
        "tanggal_selesai": "Tanggal Selesai",
        "nilai": "Nilai Kontribusi (Rp)",
        "status_aset": "Status Aset"
    },
    "Mess": {
        "nomor_surat": "No. Surat",
        "kode_aset": "Kode Aset",
        "lokasi": "Lokasi",
        "penyewa": "Penyewa",
        "keterangan": "Blok / Keterangan",
        "durasi_bulan": "Durasi (Bulan)",
        "tanggal_mulai": "Tanggal Mulai",
        "tanggal_selesai": "Tanggal Selesai",
        "nilai": "Nilai Kontribusi (Rp)",
        "status_aset": "Status Aset"
    },
    "Rumah Dinas": {
        "nomor_surat": "No. Surat",
        "kode_aset": "Kode Aset",
        "lokasi": "Alamat",
        "penyewa": "Penyewa",
        "tanggal_mulai": "Tanggal Mulai",
        "tanggal_selesai": "Tanggal Selesai",
        "nilai": "Nilai Kontribusi (Rp)",
        "status_aset": "Status Aset"
    },
}

def show():
    st.title("✍️ Input Surat Perjanjian Aset")

    df = load_aset_data()

    col1, col2 = st.columns([1, 2])

    with col1:
        jenis = st.selectbox(
            "Pilih Jenis Aset",
            list(ASET_COLUMNS.keys())
        )

    with col2:
        search = st.text_input("🔍 Cari Kode Aset / Lokasi")

    # ================= FILTER DATA =================
    df = df[df["jenis_aset"] == jenis]

    df["status_aset"] = df.apply(hitung_status_aset, axis=1)

    df["is_transaksi"] = (
        df["nomor_surat"].notna()
        & (df["nomor_surat"] != "-")
    )

    df = df.sort_values("is_transaksi", ascending=False)
    df = df.drop_duplicates(subset=["kode_aset"], keep="first")

    if search:
        df = df[
            df["kode_aset"].str.contains(search, case=False, na=False)
            | df["lokasi"].str.contains(search, case=False, na=False)
            | df["nomor_surat"].str.contains(search, case=False, na=False)
            | df["penyewa"].str.contains(search, case=False, na=False)
            | df["status_aset"].str.contains(search, case=False, na=False)
            | df["keterangan"].str.contains(search, case=False, na=False)
        ]
    df = df.sort_values(by="kode_aset", ascending=True)

    # ================= KOLOM DINAMIS =================
    mapping = ASET_COLUMNS[jenis]
    df = df[list(mapping.keys())]
    df = df.rename(columns=mapping)
    
    for col in df.columns:
        if "Tanggal" in col:
            df[col] = df[col].apply(format_tanggal_angka)

    if "Nilai Kontribusi (Rp)" in df.columns:
        df["Nilai Kontribusi (Rp)"] = df["Nilai Kontribusi (Rp)"].apply(format_rupiah)

    df = df.reset_index(drop=True)
    df.insert(0, "No", range(1, len(df) + 1))

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()