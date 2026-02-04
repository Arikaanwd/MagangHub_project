import json
import pandas as pd
import folium
from streamlit_folium import st_folium
from data_loader import load_aset_data



def load_lokasi_master(json_path="D:/MagangHub/Project/maps/lokasi_maps.json"):
    with open(json_path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df["lat"] = df["lat"].astype(float)
    df["lon"] = df["lon"].astype(float)
    df["nama_lokasi"] = df["nama_lokasi"].str.strip()
    return df

# RENDER MAP
def render_map(df_aset):
    df_lokasi = load_lokasi_master()
    df_aset = df_aset.copy()

    def normalize_nama_lokasi(text):
        if pd.isna(text):
            return None

        t = str(text).strip().lower()

        mapping = {
            # KPM
            "gedung kpm": "kpm",

            # EX KAMTIB
            "gedung ex-kam k3lh": "ex_kamtib",
            "gedung ex kam k3lh": "ex_kamtib",
            "gedung ex-kamtib": "ex_kamtib",

            # PIP
            "gedung pip lt dasar": "pip",
            "gedung pip": "pip",

            # DESAIN
            "ex. gedung div. desain": "desain",
            "ex gedung div desain": "desain",
            "div. desain": "desain",

            # KESIND
            "gedung kesind": "kesind",

            # MATERIAL
            "ex-gedung penerimaan material": "material",
            "gedung penerimaan material": "material",

            # NIAGA
            "div. kapal niaga": "niaga",

            # BELUGA
            "dok. beluga": "dok_beluga",

            # KOP KB / KOPERASI
            "gedung kop kb": "kop_kb",
            "gedung kop-kb": "kop_kb",
            "kop kb": "kop_kb",
            "gedung koperasi": "kop_kb",
            "gedung koperasi kb": "kop_kb",
        }

        return mapping.get(t, None)


    df_aset["kode_lokasi"] = df_aset["lokasi"].apply(normalize_nama_lokasi)
    df_aset["status_aset"] = df_aset["status_aset"].astype(str).str.strip()
    df_aset["jenis_aset"] = df_aset["jenis_aset"].astype(str).str.strip()

    jenis_aset_summary = (
        df_aset
        .groupby(["kode_lokasi", "jenis_aset"])
        .size()
        .reset_index(name="jumlah")
    )

    jenis_aset_summary["jenis_text"] = (
        jenis_aset_summary["jenis_aset"]
        + " (" + jenis_aset_summary["jumlah"].astype(str) + ")" + ","
    )

    jenis_aset_grouped = (
        jenis_aset_summary
        .groupby("kode_lokasi")["jenis_text"]
        .apply(lambda x: "<br>".join(x))
        .reset_index()
        .rename(columns={"kode_lokasi": "kode_lokasi"})
    )

    status_summary = (
        df_aset
        .groupby("kode_lokasi")
        .agg(
            total_aset=("status_aset", "count"),
            disewa=("status_aset", lambda x: (x == "Disewa").sum()),
            kosong=("status_aset", lambda x: (x == "Kosong").sum()),
            internal=("status_aset", lambda x: x.str.contains("Internal", case=False).sum()),
        )
        .reset_index()
        .rename(columns={"kode_lokasi": "kode_lokasi"})
    )

    df_map = (
        df_lokasi
        .merge(status_summary, on="kode_lokasi", how="left")
        .merge(jenis_aset_grouped, on="kode_lokasi", how="left")
    )

    df_map.fillna(
        {
            "total_aset": 0,
            "disewa": 0,
            "kosong": 0,
            "internal": 0,
            "jenis_text": "-"
        },
        inplace=True
    )

    # MAP
    m = folium.Map(
        location=[-7.20525726742541, 112.741479010896],
        zoom_start=15,
        tiles="OpenStreetMap"
    )

    # CSS POPUP KECIL
    css = """
    <style>
    .leaflet-popup-content {
        margin: 4px !important;
        width: 200px !important;
        font-size: 15px;
        line-height: 1.3;
    }
    .leaflet-popup-content-wrapper {
        padding: 6px !important;
        border-radius: 6px;
    }
    </style>
    """
    m.get_root().html.add_child(folium.Element(css))

    # MARKER
    for _, row in df_map.iterrows():
        popup_html = f"""
        <div>
            <b>{row['nama_lokasi']}</b><br>
            Jenis Aset : {row['jenis_text']}<br>
            Total Aset : {int(row['total_aset'])}<br>
            Disewa : {int(row['disewa'])}<br>
            Kosong : {int(row['kosong'])}<br>
            Internal : {int(row['internal'])}
        </div>
        """

        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=row["nama_lokasi"],
            icon=folium.Icon(icon="info-sign", color="blue")
        ).add_to(m)

    st_folium(m, width="100%", height=500)
