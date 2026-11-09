import sqlite3
import os

# Creamos la base de datos en la raíz del proyecto
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'hardware.db')

def obtener_conexion():
    # 1. Calculamos la ruta absoluta de la carpeta raíz del proyecto
    # Si este archivo está en app/dao/, subimos dos niveles ('..', '..')
    directorio_actual = os.path.abspath(os.path.dirname(__file__))
    ruta_raiz = os.path.abspath(os.path.join(directorio_actual, '..', '..'))
    
    # 2. Pegamos el nombre del archivo a la ruta raíz
    ruta_db = os.path.join(ruta_raiz, 'hardware.db')
    
    # 3. Conectamos (ahora es imposible que SQLite se pierda)
    return sqlite3.connect(ruta_db)

def inicializar_base_de_datos():
    """Crea las tablas necesarias si no existen."""
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        
        # Tabla de productos (URL es UNIQUE para no duplicar el mismo componente)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                tienda TEXT NOT NULL
            )
        ''')
        
        # Tabla del historial de precios (Clave foránea apuntando al producto)
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