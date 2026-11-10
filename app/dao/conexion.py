import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'hardware.db')

def obtener_conexion():
    directorio_actual = os.path.abspath(os.path.dirname(__file__))
    ruta_raiz = os.path.abspath(os.path.join(directorio_actual, '..', '..'))
    ruta_db = os.path.join(ruta_raiz, 'hardware.db')
    return sqlite3.connect(ruta_db)

def inicializar_base_de_datos():
    """Crea las tablas necesarias si no existen."""
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        
        # Tabla de productos (incluyendo la columna categoria)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                tienda TEXT NOT NULL,
                categoria TEXT DEFAULT 'General'
            )
        ''')
        
        # Tabla del historial de precios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historial_precios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto INTEGER NOT NULL,
                monto REAL NOT NULL,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_producto) REFERENCES productos (id)
            )
        ''')
        conn.commit()