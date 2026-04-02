import re

import pandas as pd
import folium
from streamlit_folium import st_folium
from branca.element import Template, MacroElement
import streamlit as st
import os
import base64

BASE_IMAGE_URL = "http://127.0.0.1:8000/storage/"

from data_loader import (
    load_master_lokasi,
    load_master_kantor,
    load_master_kontainer,
    load_master_lahan,
    load_master_mess,
    load_master_rumdin
)

warna_marker_aset = {
    "Kantor": "blue",
    "Kontainer": "orange",
    "Lahan": "green",
    "Mess": "purple",
    "Rumah Dinas": "red"
}

def generate_filename(nama_lokasi):
    nama = nama_lokasi.lower()
    nama = re.sub(r'[^a-z0-9\s]', '', nama)
    nama = nama.replace(" ", "_")
    return nama

# ===============================
@st.cache_data
def load_master_aset_semua():

    df_kantor = load_master_kantor()[["id_lokasi", "status_aset"]].copy()
    df_kantor["jenis_aset"] = "Kantor"

    df_kontainer = load_master_kontainer()[["id_lokasi", "status_aset"]].copy()
    df_kontainer["jenis_aset"] = "Kontainer"

    df_lahan = load_master_lahan()[["id_lokasi", "status_aset"]].copy()
    df_lahan["jenis_aset"] = "Lahan"

    df_mess = load_master_mess()[["id_lokasi", "status_aset"]].copy()
    df_mess["jenis_aset"] = "Mess"

    df_rumdin = load_master_rumdin()[["id_lokasi", "status_aset"]].copy()
    df_rumdin["jenis_aset"] = "Rumah Dinas"

    df_all = pd.concat(
        [df_kantor, df_kontainer, df_lahan, df_mess, df_rumdin],
        ignore_index=True
    )
    df_all["status_aset"] = df_all["status_aset"].astype(str).str.strip()

    return df_all

@st.cache_data
def load_lokasi_cached():
    return load_master_lokasi()

def render_map():
    df_lokasi = load_lokasi_cached()
    df_master_aset = load_master_aset_semua()
    jenis_aset_summary = (
        df_master_aset
        .groupby(["id_lokasi", "jenis_aset"])
        .size()
        .reset_index(name="jumlah")
    )
    jenis_aset_summary["jenis_text"] = (
        jenis_aset_summary["jenis_aset"]
        + " (" + jenis_aset_summary["jumlah"].astype(str) + ")"
    )
    jenis_aset_grouped = (
        jenis_aset_summary
        .groupby("id_lokasi")["jenis_text"]
        .apply(lambda x: "<br>".join(x))
        .reset_index()
    )
    dominant_aset = (
        jenis_aset_summary
        .sort_values("jumlah", ascending=False)
        .drop_duplicates("id_lokasi")
        [["id_lokasi", "jenis_aset"]]
        .rename(columns={"jenis_aset": "jenis_dominan"})
    )
    status_summary = (
        df_master_aset
        .groupby("id_lokasi")
        .agg(
            total_aset=("status_aset", "count"),
            disewa=("status_aset", lambda x: (x == "Disewa").sum()),
            kosong=("status_aset", lambda x: (x == "Kosong").sum()),
            internal=("status_aset", lambda x: x.str.contains("Internal", case=False).sum()),
            perbaikan=("status_aset", lambda x: x.str.contains("Perbaikan", case=False).sum()),
        )
        .reset_index()
    )
    df_map = (
        df_lokasi
        .merge(status_summary, on="id_lokasi", how="left")
        .merge(jenis_aset_grouped, on="id_lokasi", how="left")
        .merge(dominant_aset, on="id_lokasi", how="left")
    )
    df_map.fillna(0, inplace=True)
    m = folium.Map(
        location=[-7.6145292, 110.7122465],
        zoom_start=7
    )
    marker_lookup = {}
    for _, row in df_map.iterrows():
        warna = warna_marker_aset.get(row["jenis_dominan"], "gray")
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(row['nama_lokasi'], max_width=250 ),
            tooltip=row["nama_lokasi"],
            icon=folium.Icon(icon="info-sign", color=warna),
        ).add_to(m)
        marker_lookup[row["nama_lokasi"]] = row
    legend_html = """
    {% macro html(this, kwargs) %}
    <div style="position: fixed;
                bottom: 40px;
                left: 40px;
                z-index:9999;
                background:white;
                padding:12px 15px;
                border-radius:10px;
                box-shadow:0px 4px 12px rgba(0,0,0,0.3);
                font-size:14px;">
        <b>Keterangan Warna Aset</b><br><br>
    """

    for jenis, warna in warna_marker_aset.items():
        legend_html += f"""
        <div style="margin-bottom:4px;">
            <i style="background:{warna};
                    width:12px;
                    height:12px;
                    display:inline-block;
                    border-radius:50%;
                    margin-right:6px;"></i>
            {jenis}
        </div>
        """

    legend_html += "{% endmacro %}"
    macro = MacroElement()
    macro._template = Template(legend_html)
    m.get_root().add_child(macro)

    map_data = st_folium(
        m,
        key="asset_map",
        use_container_width=True,
        height=580,
        returned_objects=["last_object_clicked", "last_object_clicked_popup", "last_clicked"]
    )

    if map_data:

        clicked_object = map_data.get("last_object_clicked")
        clicked_popup = map_data.get("last_object_clicked_popup")
        clicked_map = map_data.get("last_clicked")

        if clicked_popup:
            st.session_state["selected_marker"] = clicked_popup

        elif clicked_map:
            st.session_state.pop("selected_marker", None)

        if clicked_object is None:
            st.session_state.pop("selected_marker", None)

    if st.session_state.get("selected_marker"):
        selected = st.session_state["selected_marker"]
        if selected in marker_lookup:
            row = marker_lookup[selected]
            foto_path = row.get("foto_lokasi")
            if foto_path and str(foto_path) != "0":
                image_url = BASE_IMAGE_URL + str(foto_path)
            else:
                image_url = "data:image/jpeg;base64," + base64.b64encode(
                    open(os.path.join('images', 'no-image.jpg'), 'rb').read()
                ).decode()

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
                                style="width:100%;max-height:350px;object-fit:contain;border-radius:5px;">
                        </div>
                        <div>
                            <h5 style="text-align:center;">{row['nama_lokasi']}</h5>
                            <b>Jenis Aset:</b> {row['jenis_text']}<br>
                            <b>Total Aset:</b> {int(row['total_aset'])}<br>
                            <b>Disewa:</b> {int(row['disewa'])}<br>
                            <b>Kosong:</b> {int(row['kosong'])}<br>
                            <b>Internal:</b> {int(row['internal'])}<br>
                            <b>Perbaikan:</b> {int(row['perbaikan'])}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    # ======================= 
    # panel_content = f"""
    # <div>
    #     <div style="text-align:center;margin-bottom:12px;">
    #         <img src="data:image/jpeg;base64,{encoded}"
    #                 style="width:250px;height:250px;object-fit:cover;border-radius:8px;">
    #     </div>
    #     <div>
    #         <b>{row['nama_lokasi']}</b><br><br>
    #         Jenis Aset : {row['jenis_text']}<br>
    #         Total Aset : {int(row['total_aset'])}<br>
    #         Disewa : {int(row['disewa'])}<br>
    #         Kosong : {int(row['kosong'])}<br>
    #         Internal : {int(row['internal'])}<br>
    #         Perbaikan : {int(row['perbaikan'])}
    #     </div>
    # </div>
    # """

    # panel_html = f"""
    # {{% macro html(this, kwargs) %}}
    # <div style="position: fixed;
    #             width: 350px;
    #             height: 450px;
    #             bottom: 40px;
    #             right: 40px;
    #             z-index:9999;
    #             background:white;
    #             padding:12px 15px;
    #             border-radius:10px;
    #             box-shadow:0px 1px 0px rgba(0,0,0,0.3);
    #             font-size:14px;">
    #     {panel_content}
    # </div>
    # {{% endmacro %}}
    # """

    # panel_macro = MacroElement()
    # panel_macro._template = Template(panel_html)
    # m.get_root().add_child(panel_macro)