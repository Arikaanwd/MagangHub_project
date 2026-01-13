import streamlit as st
from datetime import date
from data_loader import load_aset_data
from database import get_connection
from data_input.utils import determine_status_transaksi

if "kode_aset_lahan" not in st.session_state:
    st.session_state.kode_aset_lahan = ""
# =====================================================
# HELPER
# =====================================================
def cek_kode_lahan_exist(kode_lahan):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM master_lahan WHERE kode_lahan=%s", (kode_lahan,))
    exists = cur.fetchone()[0] > 0
    conn.close()
    return exists

def hitung_durasi_bulan(tgl_mulai_lahan, tgl_selesai_lahan):
    if not tgl_mulai_lahan or not tgl_selesai_lahan or tgl_selesai_lahan < tgl_mulai_lahan:
        return 0
    return (
        (tgl_selesai_lahan.year - tgl_mulai_lahan.year) * 12
        + (tgl_selesai_lahan.month - tgl_mulai_lahan.month)
        + 1
    )

def format_rupiah(val):
    return f"Rp {int(val or 0):,}".replace(",", ".")

def parse_rupiah(text):
    if not text:
        return 0
    return int(text.replace("Rp", "").replace(".", "").strip())

# =====================================================
# MASTER LAHAN
# =====================================================
def generate_kode_lahan():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT MAX(CAST(SUBSTRING(kode_lahan, 4) AS UNSIGNED))
        FROM master_lahan
        WHERE kode_lahan REGEXP '^LH-[0-9]+$'
    """)
    last = cur.fetchone()[0]
    conn.close()
    return f"LH-{(last or 0) + 1}"

def get_lokasi_by_kode(kode_lahan):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT lokasi FROM master_lahan WHERE kode_lahan=%s", (kode_lahan,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else ""

def get_or_create_lahan(kode_lahan, lokasi_lahan):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_lahan FROM master_lahan WHERE kode_lahan=%s", (kode_lahan,))
    row = cur.fetchone()
    if row:
        conn.close()
        return row[0]

    cur.execute("""
        INSERT INTO master_lahan
        (id_jenis_aset, kode_lahan, lokasi, status_aset)
        VALUES (4,%s,%s,'Kosong')
    """, (kode_lahan, lokasi_lahan))
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id

# =====================================================
# SESSION STATE DEFAULT
# =====================================================
fields_str = ["lokasi_lahan", "nomor_surat_lahan", "penyewa_lahan", "pic_lahan"]
fields_num = ["luas_lahan", "durasi_lahan", "nilai_raw_lahan", "tarif_air_lahan", "tarif_listrik_lahan", "tarif_sampah_lahan"]

for f in fields_str:
    st.session_state.setdefault(f, "")
for f in fields_num:
    st.session_state.setdefault(f, 0)

st.session_state.setdefault("tgl_mulai_lahan", date.today())
st.session_state.setdefault("tgl_selesai_lahan", date.today())
st.session_state.setdefault("success_submit_lahan", False)

# =====================================================
# DIALOG SUCCESS
# =====================================================
@st.dialog("✅ Data Berhasil Disimpan")
def dialog_success():
    st.success("Data SPER Lahan berhasil disimpan 🎉")

    if st.button("Tutup"):
        st.session_state.show_success_dialog_lahan = False
        st.session_state.success_submit_lahan = False
        st.rerun()
# =====================================================
# UI
# =====================================================
def show():
    st.title("INPUT SURAT PERJANJIAN LAHAN")

    if st.session_state.get("success_submit_lahan", False):
        dialog_success()

    df = load_aset_data()
    df = df[(df["jenis_aset"] == "Lahan") & (df["status_aset"] == "Kosong")]

    col1, col2 = st.columns(2)
    with col1:
        kode_list = sorted(df["kode_aset"].dropna().unique())
        pilih_kode = st.selectbox("Kode Aset Lahan", [""] + kode_list)
    with col2:
        kode_manual = st.text_input("Kode Aset Baru (Opsional)", placeholder="Kosongkan untuk auto generate")

    if pilih_kode:
        st.session_state.kode_aset_lahan = pilih_kode
        st.session_state.lokasi_lahan = get_lokasi_by_kode(pilih_kode)

    elif kode_manual.strip():
        kode_manual = kode_manual.strip().upper()
        if cek_kode_lahan_exist(kode_manual):
            st.error("Kode aset sudah digunakan")
            st.stop()
        st.session_state.kode_aset_lahan = kode_manual

    elif st.session_state.kode_aset_lahan == "":
        # AUTO GENERATE hanya sekali
        st.session_state.kode_aset_lahan = generate_kode_lahan()

    with st.form("form_lahan"):
        st.session_state.nomor_surat_lahan = st.text_input(
            "No. Surat",
            value=st.session_state.nomor_surat_lahan
        )

        col3, col4 = st.columns(2)
        with col3:
            st.session_state.penyewa_lahan = st.text_input("Penyewa", value=st.session_state.penyewa_lahan)
        with col4:
            st.session_state.lokasi_lahan = st.text_input("Lokasi", value=st.session_state.lokasi_lahan)
        col5, col6 = st.columns(2)
        with col5:
            st.session_state.luas_lahan = st.number_input(
                "Luas (m²)",
                min_value=0.0,
                value=float(st.session_state.luas_lahan)
            )
        with col6:
            st.session_state.pic = st.text_input("PIC", value= st.session_state.pic_lahan)
        col6, col7, col8 = st.columns(3)
        with col6:
            st.session_state.tgl_mulai_lahan = st.date_input(
                "Tanggal Mulai",
                value=st.session_state.tgl_mulai_lahan
            )
        with col7:
            st.session_state.tgl_selesai_lahan = st.date_input(
                "Tanggal Selesai",
                value=st.session_state.tgl_selesai_lahan
            )
        with col8:
            st.session_state.durasi_lahan = hitung_durasi_bulan(
                st.session_state.tgl_mulai_lahan,
                st.session_state.tgl_selesai_lahan
            )
            st.number_input(
                "Durasi (bulan)",
                value=st.session_state.durasi_lahan,
                disabled=True
            )
        
        keterangan = st.text_input("keterangan")

        st.divider()
        st.subheader("UTILITAS")
        col9, col10, col11 = st.columns(3)
        with col9:
            st.session_state.tarif_air_lahan = parse_rupiah(
                st.text_input("Tarif Air (Rp)", value=format_rupiah(st.session_state.tarif_air_lahan))
            )
        with col10:
            st.session_state.tarif_listrik_lahan = parse_rupiah(
                st.text_input("Tarif Listrik (Rp)", value=format_rupiah(st.session_state.tarif_listrik_lahan))
            )
        with col11:
            st.session_state.tarif_sampah_lahan = parse_rupiah(
                st.text_input("Tarif Sampah (Rp)", value=format_rupiah(st.session_state.tarif_sampah_lahan))
            )

        st.divider()

        st.subheader("Nilai Kontribusi Aset")

        st.session_state.nilai_raw_lahan = parse_rupiah(
            st.text_input(
                "Nilai Kontribusi (Rp)",
                value=format_rupiah(st.session_state.nilai_raw_lahan)
            )
        )
        st.divider()
        submitted = st.form_submit_button("💾 Simpan Data")

    if submitted:
        id_lahan = get_or_create_lahan(
            st.session_state.kode_aset_lahan,
            st.session_state.lokasi_lahan
        )
        status = determine_status_transaksi(
            st.session_state.tgl_selesai_lahan
        )

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO transaksi_lahan
            (id_lahan, nomor_surat, penyewa, luas_m2, pic_num,
             tanggal_mulai, tanggal_selesai, durasi_bulan,
             tarif_air, pem_sampah, tarif_listrik,
             nilai_kontribusi_pertahun_nonPPN, ket, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            id_lahan,
            st.session_state.nomor_surat_lahan,
            st.session_state.penyewa_lahan,
            st.session_state.luas_lahan,
            st.session_state.pic_lahan,
            st.session_state.tgl_mulai_lahan,
            st.session_state.tgl_selesai_lahan,
            st.session_state.durasi_lahan,
            st.session_state.tarif_air_lahan,
            st.session_state.tarif_sampah_lahan,
            st.session_state.tarif_listrik_lahan,
            st.session_state.nilai_raw_lahan,
            keterangan,
            status
        ))

        today = date.today()
        status_aset = (
            "Disewa"
            if st.session_state.tgl_selesai_lahan >= today
            else "Kosong"
        )

        # UPDATE MASTER LAHAN (WAJIB SELALU DIJALANKAN)
        cur.execute(
            "UPDATE master_lahan SET status_aset=%s WHERE id_lahan=%s",
            (status_aset, id_lahan)
        )

        conn.commit()
        conn.close()

        for k in fields_str + fields_num :
            st.session_state[k] ="" if k in fields_str else 0
        st.session_state.tgl_mulai_lahan = date.today()
        st.session_state.tgl_selesai_lahan = date.today()
        st.session_state.success_submit_lahan = True
        st.session_state.show_form = False
        st.rerun()
