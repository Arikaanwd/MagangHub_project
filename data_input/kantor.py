from database import get_connection
from data_input.utils import determine_status_transaksi


def insert_master_kantor(kode_kantor, lokasi, keterangan, luas_m2):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO master_kantor
        (kode_kantor, lokasi, status_aset, keterangan, luas_m2)
        VALUES (%s,%s,'Kosong',%s,%s)
    """, (kode_kantor, lokasi, keterangan, luas_m2))

    conn.commit()
    id_kantor = cur.lastrowid
    cur.close()
    conn.close()
    return id_kantor


def insert_transaksi_kantor(
    id_kantor, durasi_bulan, nomor_surat, penyewa,
    pic_num, luas_m2, tanggal_mulai,
    tanggal_selesai, nilai
):
    status = determine_status_transaksi(tanggal_selesai)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT status_aset FROM master_kantor WHERE id_kantor=%s",
        (id_kantor,)
    )
    if cur.fetchone()[0] != "Kosong":
        raise Exception("Kantor tidak boleh ditransaksikan")

    cur.execute("""
        INSERT INTO transaksi_kantor
        (id_kantor, durasi_bulan, nomor_surat, penyewa,
         pic_num, luas_m2, tanggal_mulai,
         tanggal_selesai, status,
         nilai_kontribusi_pertahun_nonPPN)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        id_kantor, durasi_bulan, nomor_surat, penyewa,
        pic_num, luas_m2, tanggal_mulai,
        tanggal_selesai, status, nilai
    ))

    if status == "Disewa":
        cur.execute(
            "UPDATE master_kantor SET status_aset='Disewa' WHERE id_kantor=%s",
            (id_kantor,)
        )

    conn.commit()
    cur.close()
    conn.close()
