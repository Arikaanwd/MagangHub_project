import streamlit as st
from datetime import date
from data_loader import load_aset_data
from database import get_connection
from data_input.utils import determine_status_transaksi




# =====================================================
# SESSION STATE INIT (ANTI RACE CONDITION)
# =====================================================
def init_state():
    defaults = {
        "alamat": "",
        "kode_aset": "",
        "nomor_surat": "",
        "penyewa": "",
        "pic": "",
        "kreditur": "",
        "luas_tanah": 0,
        "luas_bangunan": 0,
        "durasi": 0,
        "nilai_raw": 0,
        "nilai_display": "Rp 0",
        "tgl_mulai": date.today(),
        "tgl_selesai": date.today(),
        "success_submit": False,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_form_state():
    for k in list(st.session_state.keys()):
        if k != "success_submit":
            del st.session_state[k]


init_state()
# =====================================================
# MASTER STATUS
# =====================================================
def update_master_status_if_selesai():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE master_rumdin mr
        JOIN (
            SELECT id_rumdin, MAX(tanggal_selesai) AS tgl_selesai
            FROM transaksi_rumdin
            GROUP BY id_rumdin
        ) tr ON mr.id_rumdin = tr.id_rumdin
        SET mr.status_aset = 'Kosong'
        WHERE tr.tgl_selesai < CURDATE()
    """)
    conn.commit()
    conn.close()

def get_rumdin_id_by_kode(kode_rumdin):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id_rumdin FROM master_rumdin WHERE kode_rumdin=%s",
        (kode_rumdin,)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def get_rumdin_detail_by_kode(kode_rumdin):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT luas_tanah_m2, luas_bangunan_m2, kreditur
        FROM master_rumdin
        WHERE kode_rumdin = %s
    """, (kode_rumdin,))
    row = cur.fetchone()
    conn.close()
    return row

# =====================================================
# HELPER
# =====================================================
def format_rupiah(angka):
    if angka is None:
        return "Rp 0"
    return f"Rp {angka:,.0f}".replace(",", ".")

def parse_rupiah(text):
    if not text:
        return 0
    return int(text.replace("Rp", "").replace(".", "").strip())

def hitung_durasi_bulan(tgl_mulai, tgl_selesai):
    if not tgl_mulai or not tgl_selesai or tgl_selesai < tgl_mulai:
        return 0
    return ((tgl_selesai.year - tgl_mulai.year) * 12
            + (tgl_selesai.month - tgl_mulai.month) + 1)

# =====================================================
# SESSION STATE
# =====================================================
fields_str = ["alamat", "kode_aset", "nomor_surat", "penyewa", "pic", "kreditur"]
fields_num = ["luas_tanah", "luas_bangunan", "durasi", "nilai_raw"]
for f in fields_str:
    if f in st.session_state:
        del st.session_state[f]      # ✅ BOLEH DIHAPUS

for f in fields_num:
    if f in st.session_state:
        del st.session_state[f]

if "tgl_mulai" in st.session_state:
    del st.session_state["tgl_mulai"]

if "tgl_selesai" in st.session_state:
    del st.session_state["tgl_selesai"]
st.session_state.setdefault("success_submit", False)

# =====================================================
# DIALOG SUCCESS
# =====================================================
@st.dialog("✅ Data Berhasil Disimpan")
def dialog_success():
    st.markdown("### Data SPER Rumah Dinas berhasil disimpan 🎉")
    if st.button("Tutup"):
        st.session_state.success_submit = False
        st.rerun()

# =====================================================
# UI
# =====================================================
def show():
    st.title("INPUT SURAT PERJANJIAN RUMAH DINAS")

    df = load_aset_data()
    df = df[
        (df["jenis_aset"] == "Rumah Dinas") &
        (df["status_aset"] == "Kosong")
    ].copy()

    if st.session_state.success_submit:
        st.success("Data berhasil disimpan")
        if st.button("Tutup"):
            st.session_state.success_submit = False
            st.rerun()

    aset_df = df[["kode_aset", "lokasi"]].dropna().drop_duplicates().sort_values("lokasi")
    alamat_list = aset_df["lokasi"].tolist()
    alamat_to_kode = dict(zip(aset_df["lokasi"], aset_df["kode_aset"]))

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox(
            "Alamat Rumah Dinas",
            [""] + alamat_list,
            key="alamat"
        )

        if st.session_state.alamat:
            st.session_state.kode_aset = alamat_to_kode[st.session_state.alamat]

            detail = get_rumdin_detail_by_kode(st.session_state.kode_aset)
            if detail:
                st.session_state.luas_tanah = int(detail[0] or 0)
                st.session_state.luas_bangunan = int(detail[1] or 0)
                st.session_state.kreditur = detail[2] or ""
        else:
            st.session_state.kode_aset = ""

    with col2:
        st.text_input("Kode Aset (Auto-Fill)", value=st.session_state.kode_aset, disabled=True)

    if not st.session_state.alamat:
        st.info("Silakan pilih alamat rumah dinas terlebih dahulu")
        return

    # ===================== FORM =====================
    with st.form("form_rumdin"):

        st.text_input("No. Surat", key="nomor_surat")

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Penyewa", key="penyewa")
        with col2:
            st.text_input("PIC", key="pic")

        col3, col4, col5, col6, col7 = st.columns(5)

        with col3:
            st.number_input("Luas Tanah (m²)", min_value=0, key="luas_tanah")
        with col4:
            st.number_input("Luas Bangunan (m²)", min_value=0, key="luas_bangunan")
        with col5:
            st.date_input("Tanggal Mulai", key="tgl_mulai")
        with col6:
            st.date_input("Tanggal Berakhir", key="tgl_selesai")
        with col7:
            st.session_state.durasi = hitung_durasi_bulan(
                st.session_state.tgl_mulai,
                st.session_state.tgl_selesai
            )
            st.number_input("Durasi (bulan)", value=st.session_state.durasi, disabled=True)

        st.text_input("Kreditur (Jika Ada)", key="kreditur")

        st.divider()
        st.subheader("NILAI KONTRIBUSI")

        st.text_input(
            "Nilai Kontribusi (Rp)",
            value=format_rupiah(st.session_state.nilai_raw),
            key="nilai_display"
        )

        submitted = st.form_submit_button("💾 Simpan Data")

    # ===================== SUBMIT =====================
    if submitted:
        if not st.session_state.kode_aset:
            st.error("Alamat rumah dinas belum dipilih")
            st.stop()

        id_rumdin = get_rumdin_id_by_kode(st.session_state.kode_aset)
        if not id_rumdin:
            st.error("Kode aset tidak ditemukan")
            st.stop()

        status = determine_status_transaksi(st.session_state.tgl_selesai)

        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO transaksi_rumdin
                (id_rumdin, nomor_surat, penyewa, pic_number,
                luas_tanah_m2, luas_bangunan_m2,
                tanggal_mulai, tanggal_selesai,
                nilai_kontribusi_pertahun, kreditur, status)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                id_rumdin,
                st.session_state.nomor_surat,
                st.session_state.penyewa,
                st.session_state.pic,
                st.session_state.luas_tanah,
                st.session_state.luas_bangunan,
                st.session_state.tgl_mulai,
                st.session_state.tgl_selesai,
                st.session_state.nilai_raw,
                st.session_state.kreditur,
                status
            ))

            if status == "Disewa":
                cur.execute(
                    "UPDATE master_rumdin SET status_aset='Disewa' WHERE id_rumdin=%s",
                    (id_rumdin,)
                )

            conn.commit()

        except Exception as e:
            if conn:
                conn.rollback()
            st.error(f"Gagal simpan transaksi: {e}")
            st.stop()

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        # ===== Reset semua session state =====
        for f in fields_str:
            st.session_state[f] = ""
        for f in fields_num:
            st.session_state[f] = 0
        st.session_state.tgl_mulai = date.today()
        st.session_state.tgl_selesai = date.today()
        st.session_state.success_submit = True
        st.rerun()
