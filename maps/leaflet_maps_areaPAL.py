import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit as st
import base64
import os

BASE_IMAGE_URL = "https://dashboardmonitoringaset.my.id/storage/penghapusbukuan"

from data_loader import load_master_lokasi_penghapusbukuan


# ===============================
# @st.cache_data
def get_data():
    return load_master_lokasi_penghapusbukuan()

def render_map_area_PAL():
    df = get_data()

    df["status_aset"] = (
        df["status"].astype(str).str.strip().str.lower()
    )

    df = df[df["status_aset"] == "proses"]

    if df.empty:
        st.warning("Data penghapusbukuan tidak tersedia")
        return
    
    def get_latest_progress(row):
        progress_order = [
            ("Penjualan / Pemindahtanganan Aset", row["penjualan_pemindahtanganan_aset"]),
            ("SKEP Penghapusbukuan Aset", row["skep_penghapusbukuan"]),
            ("Persetujuan RUPS", row["persetujuan_rups"]),
            ("Persetujuan Fidusia (Optional)", row["persetujuan_fidusia"]),
            ("Rekomendasi / Persetujuan Dewan Komisaris", row["rekom_persetujuan_komisaris"]),
            ("Verbal Surat Direktur Utama kepada Dewan Komisaris", row["verbal_surat_dirut"]),
            ("Approval IM4 Kajian Penghapusbukuan", row["approval_im4_kajian_penghapusbukuan"]),
            ("Review Divisi Office Of The Board", row["review_div_otb"]),
            ("Kajian Manajemen Risiko dan Legal", row["kajian_manrisk_legal"]),
            ("Penerbitan LHPB", row["penerbitan_lhpb"]),
            ("Permintaan Penghapusan Aset (PPA)", row["ppa"]),
        ]
        for label, val in progress_order:
            if pd.notna(val) and str(val).strip() != "":
                return label, val
        return "Belum Ada", ""
    
    m = folium.Map(
        location=[-7.6145292, 110.7122465],
        zoom_start=7,
        max_zoom=20
    )
    marker_lookup = {}

    grouped = df.groupby(["lat", "lon"])

    for (lat, lon), group in grouped:
        first_row = group.iloc[0]
        lokasi = first_row["nama_lokasi"]
        lat = float(first_row["lat"])
        lon = float(first_row["lon"])

        jumlah_aset = len(group)
        label, value = get_latest_progress(first_row)
        nama_aset_master = first_row["nama_aset"]
        nama_aset_list = group["nama_aset_penghapusbukuan"].dropna().unique()
        nama_aset_detail = "<br>".join(nama_aset_list)

        keterangan = group["keterangan"].dropna()
        keterangan = keterangan.iloc[0] if not keterangan.empty else "-"

        key = f"{lat}_{lon}"

        tooltip_html = f"""
        <b>{lokasi}</b><br>
        {jumlah_aset} aset
        """

        popup_html = f"""
        <div style="width:200px; text-align:center;">
            <b>{lokasi}</b>
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=folium.Tooltip(tooltip_html, sticky=True),
            icon=folium.Icon(color="red", icon="trash")
        ).add_to(m)
        marker_lookup[key] = {
            "nama_aset_master": nama_aset_master,
            "nama_aset_detail": nama_aset_detail,
            "jumlah": jumlah_aset,
            "lokasi": lokasi,
            "progress_label": label,
            "progress_value": value,
            "keterangan": keterangan,
            "foto": first_row.get("foto_lokasi")
        }

    map_data = st_folium(
        m,
        key="map_pal",
        use_container_width=True,
        height=580,
        returned_objects=["last_object_clicked", "last_object_clicked_popup", "last_clicked"]
    )

    if map_data:
        clicked = map_data.get("last_object_clicked")

        if clicked:
            lat = clicked.get("lat")
            lon = clicked.get("lng")

            key = f"{lat}_{lon}"
            st.session_state["selected_marker_pal"] = key

    if st.session_state.get("selected_marker_pal"):
        selected = st.session_state["selected_marker_pal"]
        if selected in marker_lookup:
            data = marker_lookup[selected]
            
            if data["foto"] and str(data["foto"]) != "0":
                image_url = BASE_IMAGE_URL + str(data["foto"])
            else:
                no_image_path = os.path.join('images', 'no-image.jpg')
                if os.path.exists(no_image_path):
                    with open(no_image_path, 'rb') as f:
                        image_url = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
                else:
                    image_url = ""
            
            if data["jumlah"] > 1:
                nama_aset_display = f"{data['nama_aset_master']}<br>({data['jumlah']} aset)"
            else:
                nama_aset_display = data["nama_aset_master"]

            lokasi = str(data['lokasi']) if pd.notna(data['lokasi']) else "-"
            progress_label = str(data['progress_label']) if pd.notna(data['progress_label']) else "-"
            
            keterangan = data['keterangan']
            if pd.isna(keterangan) or str(keterangan).strip() == "":
                keterangan = "-"
            keterangan = str(keterangan).replace("\n", "<br>")
            
            st.markdown(
                f"""
                <div style="
                    position:absolute;
                    bottom:55px;
                    right:40px;
                    width:420px;
                    height:540px;
                    background:white;
                    padding:20px;
                    border-radius:12px;
                    box-shadow:0px 4px 12px rgba(0,0,0,0.3);
                    z-index:9999;
                    overflow-y:auto;">
                    <div>
                        <div style="text-align:center;margin-bottom:12px;">
                            <img src="{image_url}"
                                style="width:100%;max-height:400px;object-fit:contain;border-radius:5px;">
                        </div>
                        <div>
                            <h5 style="text-align:center;">{nama_aset_display}</h5>
                            <b>Lokasi :</b><br> {lokasi}<br>
                            <b>Aset : </b> <br> {data['nama_aset_detail']}<br>
                            <b>Progres :</b><br> {progress_label}<br>
                            <b>Keterangan :</b><br> {keterangan}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )