import pandas as pd

def parse_laporan_sap(filepath):
    # Baca file dengan format string agar aman
    df = pd.read_excel(filepath, dtype=str)
    df.columns = [col.strip() for col in df.columns]

    # Kolom-kolom penting
    kolom_account = 'Account Number'
    kolom_desc = 'Text for B/S P&L Item'
    kolom_now = 'Total of Reporting Period'
    kolom_prev = 'Total of the Comparison Period'
    kolom_diff = 'Absolute Difference'

    for col in [kolom_account, kolom_desc, kolom_now, kolom_prev, kolom_diff]:
        if col not in df.columns:
            raise Exception(f"Kolom '{col}' tidak ditemukan.")

    # Ambil baris yang punya account number valid
    df = df[df[kolom_account].apply(lambda x: str(x).strip().isdigit())].copy()

    # Ambil kolom lengkap
    df = df[[kolom_account, kolom_desc, kolom_now, kolom_prev, kolom_diff]]

    # Bersihkan format numerik (titik ribuan)
    for kolom in [kolom_now, kolom_prev, kolom_diff]:
        df[kolom] = df[kolom].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

    # Sort berdasarkan Account Number
    df = df.sort_values(by=kolom_account)

    return df
