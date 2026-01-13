from database import get_connection
from data_input.utils import determine_status_transaksi


def insert_master_kontainer(kode, lokasi, unit_milik, luas_m2, volume_feet):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO master_kontainer
        (kode_kontainer, lokasi, unit_milik, luas_m2, volume_feet, status_aset)
        VALUES (%s,%s,%s,%s,%s,'Kosong')
    """, (kode, lokasi, unit_milik, luas_m2, volume_feet))

    conn.commit()
    id_kontainer = cur.lastrowid
    cur.close()
    conn.close()
    return id_kontainer


def insert_transaksi_kontainer(
    id_kontainer, durasi_bulan, nomor_surat,
    penyewa, tanggal_mulai, tanggal_selesai, nilai
):
    status = determine_status_transaksi(tanggal_selesai)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT status_aset FROM master_kontainer WHERE id_kontainer=%s",
        (id_kontainer,)
    )
    if cur.fetchone()[0] != "Kosong":
        raise Exception("Kontainer tidak tersedia")

    cur.execute("""
        INSERT INTO transaksi_kontainer
        (id_kontainer, durasi_bulan, nomor_surat,
         penyewa, tanggal_mulai,
         tanggal_selesai, status,
         nilai_kontribusi_pertahun_nonPPN)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        id_kontainer, durasi_bulan, nomor_surat,
        penyewa, tanggal_mulai,
        tanggal_selesai, status, nilai
    ))

    if status == "Disewa":
        cur.execute(
            "UPDATE master_kontainer SET status_aset='Disewa' WHERE id_kontainer=%s",
            (id_kontainer,)
        )

    conn.commit()
    cur.close()
    conn.close()
