import streamlit as st
from datetime import date
from data_loader import load_aset_data
from database import get_connection
from data_input.utils import determine_status_transaksi

# ============================
# HELPER
# ============================
def cek_kode_kantor_exist(kode_aset_kantor):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM master_kantor WHERE kode_kantor=%s",
        (kode_aset_kantor,)
    )
    exists = cur.fetchone()[0] > 0
    conn.close()
    return exists

def hitung_durasi_bulan(tgl_mulai_kantor, tgl_selesai_kantor):
    if not tgl_mulai_kantor or not tgl_selesai_kantor or tgl_selesai_kantor < tgl_mulai_kantor:
        return 0
    return (tgl_selesai_kantor.year - tgl_mulai_kantor.year) * 12 + (tgl_selesai_kantor.month - tgl_mulai_kantor.month) + 1

def format_rupiah(angka):
    if angka is None:
        return "Rp 0"
    return f"Rp {angka:,.0f}".replace(",", ".")

def parse_rupiah(text):
    if not text:
        return 0
    return int(str(text).replace("Rp", "").replace(".", "").strip())

# ============================
# MASTER
# ============================
def generate_kode_kantor():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT MAX(CAST(SUBSTRING(kode_kantor, 4) AS UNSIGNED))
        FROM master_kantor
        WHERE kode_kantor REGEXP '^RK-[0-9]+$'
    """)
    last_number = cur.fetchone()[0]
    conn.close()
    return f"RK-{(last_number or 0) + 1}"

def get_lokasi_by_kode_aset(kode_aset_kantor):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT lokasi FROM master_kantor WHERE kode_kantor=%s", (kode_aset_kantor,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else ""

def get_or_create_kantor(kode_aset, lokasi_kantor):
    conn = get_connection()
    cur = conn.cursor()

    # CEK EXIST
    cur.execute(
        "SELECT id_kantor FROM master_kantor WHERE kode_kantor=%s",
        (kode_aset,)
    )
    row = cur.fetchone()

    if row:
        conn.close()
        return row[0]

    # INSERT BARU
    cur.execute("""
        INSERT INTO master_kantor
        (id_jenis_aset, kode_kantor, lokasi, status_aset, keterangan)
        VALUES (1, %s, %s, 'Kosong', '')
    """, (kode_aset, lokasi_kantor))

    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id

# ============================
# DIALOG SUCCESS
# ============================
@st.dialog("✅ Data Berhasil Disimpan")
def dialog_success():
    st.markdown("### Data SPER Mess berhasil disimpan 🎉")
    if st.button("Tutup"):
        st.session_state.success_submit_kantor = False
        st.rerun()

# ============================
# SESSION STATE DEFAULT
# ============================
fields_str = ["lokasi_kantor", "nomor_surat_kantor", "penyewa_kantor", "pic_kantor"]
fields_num = ["luas_kantor", "durasi_kantor", "nilai_raw_kantor", "tarif_air_kantor", "tarif_listrik_kantor", "tarif_sampah_kantor"]

for f in fields_str:
    st.session_state.setdefault(f, "")
for f in fields_num:
    st.session_state.setdefault(f, 0)

st.session_state.setdefault("tgl_mulai_kantor", date.today())
st.session_state.setdefault("tgl_selesai_kantor", date.today())
st.session_state.setdefault("success_submit_kantor", False)
st.session_state.setdefault("show_form", False)  # form tersembunyi awal

# ============================
# UI
# ============================
def show():
    st.title("INPUT SURAT PERJANJIAN KANTOR")

    # Tampilkan dialog jika data baru disimpan
    if st.session_state.get("success_submit_kantor", False):
        dialog_success()

    # Load data aset
    df = load_aset_data()
    df = df[(df["jenis_aset"] == "Kantor") & (df["status_aset"] == "Kosong")]
    kode_master_kantor = sorted(df["kode_aset"].dropna().unique())

    # Pilihan kode
    col1, col2 = st.columns(2)
    with col1:
        pilihan_kode_kantor = st.selectbox("Kode Aset Kantor", [""] + kode_master_kantor)
    with col2:
        kode_manual_kantor = st.text_input("Kode Aset Baru (Opsional)", placeholder="Kosongkan untuk auto generate")
    
    # if not pilihan_kode:
    #     st.info("Silakan pilih atau buat kode aset terlebih dahulu")
    #     return

    # # Hanya tampilkan form jika kode sudah dipilih atau diketik
    # if pilihan_kode or kode_manual.strip():
    #     st.session_state.show_form = True
    
    # if st.session_state.show_form:
    if pilihan_kode_kantor:
        kode_aset = pilihan_kode_kantor
        st.session_state.lokasi_kantor = get_lokasi_by_kode_aset(pilihan_kode_kantor)
    elif kode_manual_kantor.strip():
        kode_aset_kantor = kode_manual_kantor.strip().upper()
        if cek_kode_kantor_exist(kode_aset_kantor):
            st.error("Kode aset sudah digunakan")
            st.stop()
    else:
        kode_aset_kantor = generate_kode_kantor()

    # ============================
    # FORM
    # ============================
    with st.form("form_kantor"):
        st.text_input("No. Surat", value=st.session_state.get("nomor_surat_kantor", ""))
        
        col3, col4, col5 = st.columns(3)
        with col3:
            st.session_state.lokasi_kantor = st.text_input("Lokasi", value=st.session_state.lokasi_kantor)
        with col4:
            st.text_input("Penyewa", key="penyewa_kantor")
        with col5:
            st.text_input("PIC", key="pic")

        col6, col7, col8, col9 = st.columns(4)
        with col6:
            st.number_input("Luas (m²)", key="luas_kantor", min_value=0.0, step=1.0)
        with col7:
            st.date_input("Tanggal Mulai", key="tgl_mulai_kantor")
        with col8:
            st.date_input("Tanggal Selesai", key="tgl_selesai_kantor")
        with col9:
            st.session_state.durasi_kantor = hitung_durasi_bulan(st.session_state.tgl_mulai_kantor, st.session_state.tgl_selesai_kantor)
            st.number_input("Durasi (bulan)", value=st.session_state.durasi_kantor, disabled=True)

        st.divider()
        st.subheader("UTILITAS")
        col12, col13, col14 = st.columns(3)
        with col12:
            st.session_state.tarif_air_kantor = parse_rupiah(st.text_input("Tarif Air (Rp)", value=format_rupiah(st.session_state.tarif_air_kantor)))
        with col13:
            st.session_state.tarif_listrik_kantor = parse_rupiah(st.text_input("Tarif Listrik (Rp)", value=format_rupiah(st.session_state.tarif_listrik_kantor)))
        with col14:
            st.session_state.tarif_sampah_kantor = parse_rupiah(st.text_input("Tarif Sampah (Rp)", value=format_rupiah(st.session_state.tarif_sampah_kantor)))

        st.divider()
        st.subheader("Nilai Kontribusi Aset")

        st.session_state.nilai_raw_kantor = parse_rupiah(st.text_input("Nilai Kontribusi (Rp)", value=format_rupiah(st.session_state.nilai_raw_kantor)))

        st.divider()
        submitted = st.form_submit_button("💾 Simpan Data")

    if submitted:
        # Simpan data ke DB
        id_kantor = get_or_create_kantor(kode_aset_kantor, st.session_state.lokasi_kantor)
        status = determine_status_transaksi(st.session_state.tgl_selesai_kantor)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO transaksi_kantor
            (id_kantor, nomor_surat, penyewa, pic_num, luas_m2,
            tanggal_mulai, tanggal_selesai, durasi_bulan,
            tarif_air, tarif_listrik, pem_sampah,
            nilai_kontribusi_pertahun_nonPPN, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            id_kantor,
            st.session_state.nomor_surat_kantor,
            st.session_state.penyewa_kantor,
            st.session_state.pic_kantor,
            st.session_state.luas_kantor,
            st.session_state.tgl_mulai_kantor,
            st.session_state.tgl_selesai_kantor,
            st.session_state.durasi_kantor,
            st.session_state.tarif_air_kantor,
            st.session_state.tarif_listrik_kantor,
            st.session_state.tarif_sampah_kantor,
            st.session_state.nilai_raw_kantor,
            status
        ))

        if status == "Disewa":
            cur.execute("UPDATE master_kantor SET status_aset='Disewa' WHERE id_kantor=%s", (id_kantor,))

        conn.commit()
        conn.close()

        # Reset session state setelah submit
        for f in fields_str + fields_num:
            st.session_state[f] = "" if f in fields_str else 0
        st.session_state.tgl_mulai_kantor = date.today()
        st.session_state.tgl_selesai_kantor = date.today()
        st.session_state.success_submit_kantor = True
        st.session_state.show_form = False  # sembunyikan form setelah submit
        st.rerun()
