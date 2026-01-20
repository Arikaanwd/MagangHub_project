import streamlit as st
from datetime import date
from data_loader import load_aset_data
from database import get_connection
from data_input.utils import determine_status_transaksi

# =====================================================
# MASTER STATUS
# =====================================================
def update_master_status_if_selesai():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE master_kontainer mk
        JOIN (
            SELECT id_kontainer, MAX(tanggal_selesai) AS tgl_selesai
            FROM transaksi_kontainer
            GROUP BY id_kontainer
        ) tr ON mk.id_kontainer = tr.id_kontainer
        SET mk.status_aset = 'Kosong'
        WHERE tr.tgl_selesai < CURDATE()
    """)
    conn.commit()
    conn.close()

def update_master_status_disewa(id_kontainer_kontainer):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE master_kontainer SET status_aset='Disewa' WHERE id_kontainer=%s",
        (id_kontainer_kontainer,)
    )
    conn.commit()
    conn.close()

# =====================================================
# HELPER
# =====================================================
def hitung_durasi_bulan(tgl_mulai_kontainer, tgl_selesai_kontainer):
    if not tgl_mulai_kontainer or not tgl_selesai_kontainer or tgl_selesai_kontainer < tgl_mulai_kontainer:
        return 0
    return (
        (tgl_selesai_kontainer.year - tgl_mulai_kontainer.year) * 12
        + (tgl_selesai_kontainer.month - tgl_mulai_kontainer.month)
        + 1
    )
def format_rupiah(angka):
    return f"Rp {int(angka or 0):,}".replace(",", ".")
def parse_rupiah(text):
    if not text:
        return 0
    return int(text.replace("Rp", "").replace(".", "").strip())
# =====================================================
# MASTER KONTAINER
# =====================================================
def generate_kode_kontainer():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT MAX(CAST(SUBSTRING(kode_kontainer,4) AS UNSIGNED))
        FROM master_kontainer
        WHERE kode_kontainer LIKE 'PK-%'
        FOR UPDATE
    """)
    last = cur.fetchone()[0]
    conn.close()
    return f"PK-{(last or 0) + 1}"

def get_kontainer_by_kode(kode_aset_kontainer):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT id_kontainer, lokasi, volume_feet, luas_m2, unit_milik
        FROM master_kontainer
        WHERE kode_kontainer=%s
    """, (kode_aset_kontainer,))
    row = cur.fetchone()
    conn.close()
    return row 

def get_or_create_kontainer(kode_aset_kontainer, lokasi_kontainer, volume_kontainer, luas_kontainer, unit_kontainer):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id_kontainer FROM master_kontainer WHERE kode_kontainer=%s",
        (kode_aset_kontainer,)
    )
    row = cur.fetchone()
    if row:
        conn.close()
        return row[0]

    cur.execute("""
        INSERT INTO master_kontainer
        (id_jenis_aset, kode_kontainer, volume_feet, luas_m2,
         lokasi, unit_milik, status_aset)
        VALUES (5,%s,%s,%s,%s,%s,'Kosong')
    """, (kode_aset_kontainer, volume_kontainer, luas_kontainer, lokasi_kontainer, unit_kontainer))
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id

# =====================================================
# SESSION STATE
# =====================================================
defaults = {
    "success_submit_kontainer": False,
    "kode_kontainer": "",
    "lokasi_kontainer": "",
    "volume_kontainer": 0.0,
    "luas_kontainer": 0.0,
    "unit_milik_kontainer": "",
    "nomor_surat_kontainer": "",
    "penyewa_kontainer": "",
    "tgl_mulai_kontainer": date.today(),
    "tgl_selesai_kontainer": date.today(),
    "nilai_raw_kontainer": 0,
    "pem_sampah_kontainer": 0,
    "nilai_lahan_kontainer": 0,
    "show_form": False
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)

st.session_state.setdefault("tgl_mulai_kontainer", date.today())
st.session_state.setdefault("tgl_selesai_kontainer", date.today())
st.session_state.setdefault("success_submit_kontainer", False)
# =====================================================
# DIALOG SUCCESS
# =====================================================
@st.dialog("✅ Data Berhasil Disimpan")
def dialog_success():
    st.markdown("### Data SPER Mess berhasil disimpan 🎉")
    if st.button("Tutup"):
        st.session_state.success_submit_kontainer = False
        st.rerun()

st.session_state.setdefault("success_submit_kontainer", False)

def reset_form():
    for k, v in defaults.items():
        st.session_state[k] = v
# =====================================================
# UI
# =====================================================
def show():
    update_master_status_if_selesai()
    st.title("INPUT SURAT PERJANJIAN KONTAINER")

    if st.session_state.get("success_submit_kontainer", False):
        dialog_success()

    df = load_aset_data()
    df = df[(df["jenis_aset"] == "Kontainer") & (df["status_aset"] == "Kosong")]

    col1, col2 = st.columns(2)
    with col1:
        kode_list = sorted(df["kode_aset"].dropna().unique())
        pilih_kode = st.selectbox("Kode Aset Kontainer", [""] + kode_list)
    with col2:
        manual_kode = st.text_input("Kode Manual (opsional)", placeholder="Kosongkan untuk auto generate")

    if pilih_kode:
        kode_final = pilih_kode
        data = get_kontainer_by_kode(pilih_kode)
        if data:
            st.session_state.lokasi_kontainer = data["lokasi"]
            st.session_state.volume_kontainer = float(data["volume_feet"] or 0)
            st.session_state.luas_kontainer = float(data["luas_m2"] or 0)
            st.session_state.unit_milik_kontainer = data["unit_milik"] or ""

    elif manual_kode.strip():
        kode_final = manual_kode.strip().upper()

    else:
        kode_final = generate_kode_kontainer()

    st.session_state.kode_kontainer = kode_final
    st.session_state.show_form = True
    
    with st.form("form_kontainer"): 
        # tambahkan colom
        st.session_state.nomor_surat_kontainer = st.text_input("No. Surat")
        
        col3, col4 = st.columns(2)
        with col3:
            st.session_state.penyewa_kontainer = st.text_input("Penyewa")
        with col4:
            st.text_input("Lokasi", key="lokasi_kontainer")

        col5, col6, col7 = st.columns(3)    
        with col5:
            st.session_state.volume_kontainer = st.number_input("Volume (Feet)", value=float(st.session_state.volume_kontainer or 0), min_value=0.0)
        with col6:
            st.session_state.luas_kontainer = st.number_input("Luas (m²)", value=float(st.session_state.luas_kontainer or 0), min_value=0.0)
        with col7:
            st.session_state.unit_milik_kontainer = st.text_input("Unit Milik", value=st.session_state.unit_milik_kontainer)

        col8, col9, col10 = st.columns(3)
        with col8:
            st.date_input("Tanggal Mulai", key="tgl_mulai_kontainer")
        with col9:
            st.date_input("Tanggal Selesai", key="tgl_selesai_kontainer")
        with col10:
            durasi = hitung_durasi_bulan(st.session_state.tgl_mulai_kontainer, st.session_state.tgl_selesai_kontainer)
            st.number_input("Durasi (bulan)", value=durasi, disabled=True)
        st.divider()
        
        st.subheader("UTILITAS")
        col11, col12 = st.columns(2)
        with col11:
            st.session_state.pem_sampah_kontainer = parse_rupiah(
                st.text_input("Tarif Sampah (Rp)", value=format_rupiah(st.session_state.pem_sampah_kontainer))
            )
        with col12:    
            st.session_state.nilai_lahan_kontainer = parse_rupiah(
                st.text_input("Tarif Lahan (Rp)", value=format_rupiah(st.session_state.nilai_lahan_kontainer))
            )
        st. divider()
        st.subheader("Nilai Kontribusi Aset")
        st.session_state.nilai_raw_kontainer = parse_rupiah(
            st.text_input("Nilai Kontribusi (Rp)", value=format_rupiah(st.session_state.nilai_raw_kontainer))
        )
        st.divider()
        submitted = st.form_submit_button("💾 Simpan Data")

    if submitted:
        id_kontainer = get_or_create_kontainer(
            st.session_state.kode_kontainer,
            st.session_state.lokasi_kontainer,
            st.session_state.volume_kontainer,
            st.session_state.luas_kontainer,
            st.session_state.unit_milik_kontainer
        )

        status = determine_status_transaksi(st.session_state.tgl_selesai_kontainer)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO transaksi_kontainer
            (id_kontainer, nomor_surat, penyewa,
             tanggal_mulai, tanggal_selesai, durasi_bulan,
             pem_sampah, nilai_kontribusi_lahan_perbulan,
             nilai_kontribusi_pertahun_nonPPN, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            id_kontainer,
            st.session_state.nomor_surat_kontainer,
            st.session_state.penyewa_kontainer,
            st.session_state.tgl_mulai_kontainer,
            st.session_state.tgl_selesai_kontainer,
            durasi,
            st.session_state.pem_sampah_kontainer,
            st.session_state.nilai_lahan_kontainer,
            st.session_state.nilai_raw_kontainer,
            status
        ))

        conn.commit()
        conn.close()
        update_master_status_disewa(id_kontainer)

        reset_form()

        st.session_state.success_submit_kontainer = True
        st.session_state.show_form = False
        st.rerun()
