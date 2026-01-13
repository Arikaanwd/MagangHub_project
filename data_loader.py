import pandas as pd
import re
from database import fetch


def extract_year_from_nomor_surat(nomor):
    if pd.isna(nomor):
        return None
    match = re.search(r"(20\d{2})", str(nomor))
    return int(match.group(1)) if match else None


def load_aset_data():
    query = """
    SELECT 
        'Kantor' AS jenis_aset,
        mk.kode_kantor AS kode_aset,
        mk.lokasi,
        mk.status_aset AS status_aset,
        mk.keterangan,
        tk.durasi_bulan,
        tk.nomor_surat,
        tk.penyewa,
        tk.pic_num,
        tk.luas_m2,
        tk.tanggal_mulai,
        tk.tanggal_selesai,
        NULL AS volume_feet,
        NULL AS nilai_kontribusi_perbulan,
        tk.no_surat_addendum AS surat_addendum,
        CAST(COALESCE(tk.nilai_kontribusi_pertahun_nonPPN, 0) AS DECIMAL(15,2)) AS nilai
    FROM master_kantor mk
    JOIN transaksi_kantor tk ON mk.id_kantor = tk.id_kantor

    UNION ALL

    SELECT 
        'Kontainer' AS jenis_aset,
        mt.kode_kontainer,
        mt.lokasi,
        mt.status_aset,
        mt.unit_milik AS keterangan,
        kt.durasi_bulan,
        kt.nomor_surat,
        kt.penyewa,
        NULL,
        mt.luas_m2,
        kt.tanggal_mulai,
        kt.tanggal_selesai,
        mt.volume_feet,
        NULL,
        NULL,
        CAST(COALESCE(kt.nilai_kontribusi_pertahun_nonPPN, 0) AS DECIMAL(15,2))
    FROM master_kontainer mt
    JOIN transaksi_kontainer kt ON mt.id_kontainer = kt.id_kontainer
    

    UNION ALL

    SELECT 
        'Lahan' AS jenis_aset,
        ml.kode_lahan,
        ml.lokasi,
        ml.status_aset,
        tl.ket AS keterangan,
        tl.durasi_bulan,
        tl.nomor_surat,
        tl.penyewa,
        tl.pic_num,
        tl.luas_m2,
        tl.tanggal_mulai,
        tl.tanggal_selesai,
        NULL,
        NULL,
        NULL,
        CAST(COALESCE(tl.nilai_kontribusi_pertahun_nonPPN, 0) AS DECIMAL(15,2))
    FROM master_lahan ml
    JOIN transaksi_lahan tl ON ml.id_lahan = tl.id_lahan

    UNION ALL

    SELECT 
        'Mess' AS jenis_aset,
        mm.kode_mess,
        tm.unit_kerja,
        mm.status_aset,
        mm.Blok AS keterangan,
        tm.durasi_bulan,
        tm.nomor_surat,
        tm.penyewa,
        NULL,
        NULL,
        tm.tanggal_mulai,
        tm.tanggal_selesai,
        NULL,
        CAST(COALESCE(tm.nilai_kontribusi_perbulan, 0) AS DECIMAL(15,2)),
        NULL,
        CAST(COALESCE(tm.nilai_kontribusi_perbulan, 0) * tm.durasi_bulan AS DECIMAL(15,2))
    FROM master_mess mm
    LEFT JOIN transaksi_mess tm ON mm.id_mess = tm.id_mess

    UNION ALL

    SELECT 
        'Rumah Dinas' AS jenis_aset,
        mr.kode_rumdin,
        mr.alamat,
        mr.status_aset,
        tr.kreditur AS keterangan,
        NULL,
        tr.nomor_surat,
        tr.penyewa,
        tr.pic_number,
        NULL,
        tr.tanggal_mulai,
        tr.tanggal_selesai,
        NULL,
        NULL,
        NULL,
        CAST(COALESCE(tr.nilai_kontribusi_pertahun, 0) AS DECIMAL(15,2))
    FROM master_rumdin mr
    JOIN transaksi_rumdin tr ON mr.id_rumdin = tr.id_rumdin
    """

    data, columns = fetch(query)
    df = pd.DataFrame(data, columns=columns)

    # ================== NORMALISASI ==================
    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce").fillna(0)

    df["durasi_bulan"] = pd.to_numeric(
        df["durasi_bulan"], errors="coerce"
    ).fillna(0).astype("Int64")

    df["tanggal_mulai"] = pd.to_datetime(df["tanggal_mulai"], errors="coerce")
    df["tanggal_selesai"] = pd.to_datetime(df["tanggal_selesai"], errors="coerce")

    # Tahun DIAMBIL DARI NOMOR SURAT (SESUSAI KEBUTUHAN ANDA)
    df["tahun"] = df["nomor_surat"].apply(extract_year_from_nomor_surat)

    df["keterangan"] = df["keterangan"].fillna("")

    return df
