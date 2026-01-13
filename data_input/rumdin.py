from database import get_connection
from data_input.utils import determine_status_transaksi


def insert_master_rumdin(kode_rumdin, alamat):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO master_rumdin
        (kode_rumdin, alamat, status_aset)
        VALUES (%s,%s,'Kosong')
    """, (kode_rumdin, alamat))

    conn.commit()
    id_rumdin = cur.lastrowid
    cur.close()
    conn.close()
    return id_rumdin


def insert_transaksi_rumdin(
    id_rumdin, nomor_surat, penyewa,
    kreditur, pic_number,
    tanggal_mulai, tanggal_selesai, nilai
):
    status = determine_status_transaksi(tanggal_selesai)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT status_aset FROM master_rumdin WHERE id_rumdin=%s",
        (id_rumdin,)
    )
    if cur.fetchone()[0] != "Kosong":
        raise Exception("Rumah dinas tidak tersedia")

    cur.execute("""
        INSERT INTO transaksi_rumdin
        (id_rumdin, nomor_surat, penyewa,
         kreditur, pic_number,
         tanggal_mulai, tanggal_selesai,
         status, nilai_kontribusi_pertahun)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        id_rumdin, nomor_surat, penyewa,
        kreditur, pic_number,
        tanggal_mulai, tanggal_selesai,
        status, nilai
    ))

    if status == "Disewa":
        cur.execute(
            "UPDATE master_rumdin SET status_aset='Disewa' WHERE id_rumdin=%s",
            (id_rumdin,)
        )

    conn.commit()
    cur.close()
    conn.close()
