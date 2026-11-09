import sqlite3
import os

ruta_db = os.path.abspath(os.path.join(os.path.dirname(__file__), 'hardware.db'))
with sqlite3.connect(ruta_db) as conn:
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE productos ADD COLUMN categoria TEXT DEFAULT 'General'")
        print("Columna 'categoria' agregada con éxito a la tabla de productos.")
    except sqlite3.OperationalError:
        print("La columna 'categoria' ya existe.")