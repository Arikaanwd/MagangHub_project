# filters.py
def apply_global_filters(df, tahun=None, jenis_aset=None, penyewa=None):

    if tahun:
        df = df[df["tahun"].isin(tahun)]

    if jenis_aset:
        df = df[df["jenis_aset"].isin(jenis_aset)]

    if penyewa:
        df = df[df["penyewa"].isin(penyewa)]

    return df
