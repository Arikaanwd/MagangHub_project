from database import fetch, execute

def generate_kode(prefix, table, column):
    query = f"""
        SELECT {column}
        FROM {table}
        WHERE {column} LIKE '{prefix}-%'
        ORDER BY {column} DESC
        LIMIT 1
    """
    data, _ = fetch(query)

    if not data:
        return f"{prefix}-01"

    last_code = data[0][0]
    last_num = int(last_code.split("-")[-1])
    return f"{prefix}-{last_num + 1:02d}"
