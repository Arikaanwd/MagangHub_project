from database import get_connection
from data_input.utils import determine_status_transaksi


def insert_master_mess(kode_mess, unit_kerja, blok):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO master_mess
        (kode_mess, unit_kerja, Blok, status_aset)
        VALUES (%s,%s,%s,'Kosong')
    """, (kode_mess, unit_kerja, blok))

    conn.commit()
    id_mess = cur.lastrowid
    cur.close()
    conn.close()
    return id_mess


def insert_transaksi_mess(
    id_mess, durasi_bulan, nomor_surat,
    penyewa, tanggal_mulai, tanggal_selesai,
    nilai_bulanan
):
    status = determine_status_transaksi(tanggal_selesai)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT status_aset FROM master_mess WHERE id_mess=%s",
        (id_mess,)
    )
    if cur.fetchone()[0] != "Kosong":
        raise Exception("Mess tidak tersedia")

    cur.execute("""
        INSERT INTO transaksi_mess
        (id_mess, durasi_bulan, nomor_surat,
         penyewa, tanggal_mulai,
         tanggal_selesai, status,
         nilai_kontribusi_perbulan)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        id_mess, durasi_bulan, nomor_surat,
        penyewa, tanggal_mulai,
        tanggal_selesai, status, nilai_bulanan
    ))

    if status == "Disewa":
        cur.execute(
            "UPDATE master_mess SET status_aset='Disewa' WHERE id_mess=%s",
            (id_mess,)
        )

    conn.commit()
    cur.close()
    conn.close()
