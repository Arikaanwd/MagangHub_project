import streamlit as st
from datetime import date
from data_loader import load_aset_data
from database import get_connection
from data_input.utils import determine_status_transaksi


# =====================================================
# HELPER
# =====================================================
def hitung_durasi_bulan(tgl_mulai, tgl_selesai):
    if not tgl_mulai or not tgl_selesai:
        return 0
    if tgl_selesai < tgl_mulai:
        return 0
    return (
        (tgl_selesai.year - tgl_mulai.year) * 12
        + (tgl_selesai.month - tgl_mulai.month)
        + 1
    )


def format_rupiah(angka):
    if angka is None:
        return "Rp 0"
    return f"Rp {angka:,.0f}".replace(",", ".")


def parse_rupiah(text):
    if not text:
        return 0
    return int(text.replace("Rp", "").replace(".", "").strip())


def get_id_mess_by_kode(kode_mess):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id_mess FROM master_mess WHERE kode_mess=%s",
        (kode_mess,)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

# =====================================================
# DIALOG
# =====================================================
@st.dialog("✅ Data Berhasil Disimpan")
def dialog_success():
    st.markdown("### Data SPER Mess berhasil disimpan 🎉")
    if st.button("Tutup"):
        st.session_state.success_submit = False
        st.rerun()

# =====================================================
# SESSION STATE
# =====================================================
for k, v in {
    "success_submit_mess": False,
    "nilai_raw": 0,
}.items():
    st.session_state.setdefault(k, v)

# st.session_state.setdefault("success_submit", False)
# =====================================================
# UI
# =====================================================
def show():
    st.title("INPUT SURAT PERJANJIAN MESS MENANGGAL")

    if st.session_state.get("success_submit_mess", False):
        dialog_success()

    # ================= LOAD DATA =================
    df = load_aset_data()
    df = df[
        (df["jenis_aset"] == "Mess") &
        (df["status_aset"] == "Kosong")
    ].copy()

    if df.empty:
        st.warning("Tidak ada mess dengan status Kosong")
        return
    
    # ================= PILIH BLOK (DI LUAR FORM) =================
    blok_list = sorted(df["keterangan"].dropna().unique())
    blok = st.selectbox("Blok / Kamar", [""] + blok_list)

    kode_aset = ""
    if blok:
        row = df[df["keterangan"] == blok].iloc[0]
        kode_aset = row["kode_aset"]

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Kode Aset Mess", value=kode_aset, disabled=True)
    with col2:
        lantai = st.text_input("Lantai", value="", disabled=True)
       
    if not blok:
        st.info("Silakan pilih Blok/Kamar terlebih dahulu")
        return

    # ================= FORM =================
    with st.form("form_mess"):
        nomor_surat = st.text_input("No. Surat")
        col3, col4 = st.columns(2)
        with col3:
            # Unit kerja tetap kosong agar user isi manual
            unit_kerja = st.text_input("Unit Kerja", value="")
        with col4:
            penyewa = st.text_input("Penyewa")

        col5, col6, col7 = st.columns(3)
        with col5:
            tgl_mulai = st.date_input("Tanggal Mulai")
        with col6:
            tgl_selesai = st.date_input("Tanggal Selesai")
        with col7:
            durasi = hitung_durasi_bulan(tgl_mulai, tgl_selesai)
            st.number_input(
                "Durasi Kontrak (bulan)",
                value=durasi,
                disabled=True
            )

        st.divider()
        st.subheader("NILAI KONTRIBUSI ASET")

        nilai_text = st.text_input(
            "Nilai Kontribusi (Rp)",
            value=format_rupiah(st.session_state.nilai_raw)
        )
        kontribusi_bulan = parse_rupiah(nilai_text)
        st.session_state.nilai_raw = kontribusi_bulan

        st.divider()

        submitted = st.form_submit_button("💾 Simpan Data")

    # ================= SUBMIT =================
    if submitted:
        if not kode_aset:
            st.error("Blok/Kamar belum dipilih")
            st.stop()
        if not unit_kerja.strip():
            st.error("Unit Kerja harus diisi")
            st.stop()

        id_mess = get_id_mess_by_kode(kode_aset)
        status = determine_status_transaksi(tgl_selesai)

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO transaksi_mess
            (id_mess, nomor_surat, penyewa,unit_kerja,
             tanggal_mulai, tanggal_selesai,
             durasi_bulan, nilai_kontribusi_perbulan, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            id_mess,
            nomor_surat,
            penyewa,
            unit_kerja,
            tgl_mulai,
            tgl_selesai,
            durasi,
            kontribusi_bulan,
            status
        ))

        if status == "Disewa":
            cur.execute(
                "UPDATE master_mess SET status_aset='Disewa' WHERE id_mess=%s",
                (id_mess,)
            )

        conn.commit()
        conn.close()

        st.session_state.success_submit_mess = True
        st.session_state.nilai_raw = 0
        st.rerun()
