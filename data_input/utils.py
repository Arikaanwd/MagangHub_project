from datetime import date

def determine_status_transaksi(tanggal_selesai):
    if tanggal_selesai and date.today() > tanggal_selesai:
        return "Selesai"
    return "Disewa"


# ===========================
# DITAMBAHKAN
# ===========================
def update_master_status_if_selesai(
    cur,
    table_master,
    pk_column,
    pk_value,
    status
):
    """
    Jika transaksi selesai → status master kembali Kosong
    """
    if status == "Selesai":
        cur.execute(
            f"""
            UPDATE {table_master}
            SET status_aset = 'Kosong'
            WHERE {pk_column} = %s
            """,
            (pk_value,)
        )