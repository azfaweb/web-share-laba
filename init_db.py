import sqlite3

conn = sqlite3.connect('share_laba.db')
c = conn.cursor()

# Tabel user: username, password (plain untuk sekarang), role (admin/partner)
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')

# Tabel log audit
c.execute('''
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        filename TEXT,
        total_laba REAL,
        ip_address TEXT,
        username TEXT
    )
''')

# Tambah user admin & partner (sementara hardcoded)
c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('partner', 'partner123', 'partner')")

conn.commit()
conn.close()
print("✅ Database berhasil diinisialisasi.")
