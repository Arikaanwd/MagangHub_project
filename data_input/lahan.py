from database import get_connection
from data_input.utils import determine_status_transaksi


def insert_master_lahan(kode_lahan, lokasi):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO master_lahan
        (kode_lahan, lokasi, status_aset)
        VALUES (%s,%s,'Kosong')
    """, (kode_lahan, lokasi))

    conn.commit()
    id_lahan = cur.lastrowid
    cur.close()
    conn.close()
    return id_lahan


def insert_transaksi_lahan(
    id_lahan, durasi_bulan, nomor_surat,
    penyewa, ket, luas_m2,
    tanggal_mulai, tanggal_selesai, nilai
):
    status = determine_status_transaksi(tanggal_selesai)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT status_aset FROM master_lahan WHERE id_lahan=%s",
        (id_lahan,)
    )
    if cur.fetchone()[0] != "Kosong":
        raise Exception("Lahan tidak tersedia")

    cur.execute("""
        INSERT INTO transaksi_lahan
        (id_lahan, durasi_bulan, nomor_surat,
         penyewa, ket, luas_m2,
         tanggal_mulai, tanggal_selesai,
         status, nilai_kontribusi_pertahun_nonPPN)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        id_lahan, durasi_bulan, nomor_surat,
        penyewa, ket, luas_m2,
        tanggal_mulai, tanggal_selesai,
        status, nilai
    ))

    if status == "Disewa":
        cur.execute(
            "UPDATE master_lahan SET status_aset='Disewa' WHERE id_lahan=%s",
            (id_lahan,)
        )

    conn.commit()
    cur.close()
    conn.close()
