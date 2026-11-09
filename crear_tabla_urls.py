import sqlite3
import os

ruta_db = os.path.abspath(os.path.join(os.path.dirname(__file__), 'hardware.db'))
with sqlite3.connect(ruta_db) as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls_monitoreadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
print("Tabla 'urls_monitoreadas' lista para usarse.")