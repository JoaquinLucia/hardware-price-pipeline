import sqlite3

class HardwareDAO:
    """Data Access Object exclusivo para operaciones de base de datos."""
    
    def __init__(self, nombre_db="hardware_pipeline.db"):
        self.nombre_db = nombre_db
        self._crear_tabla()

    def _conectar(self):
        return sqlite3.connect(self.nombre_db)

    def _crear_tabla(self):
        query = """
        CREATE TABLE IF NOT EXISTS precios_hardware (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            precio REAL NOT NULL,
            fecha_registro TEXT NOT NULL
        )
        """
        try:
            with self._conectar() as conexion:
                cursor = conexion.cursor()
                cursor.execute(query)
                conexion.commit()
        except sqlite3.Error as e:
            print(f"[DAO] Error al inicializar DB: {e}")

    def insertar(self, componente):
        """Inserta el componente en la BD. Retorna True si fue exitoso, o lanza excepción."""
        query = """
        INSERT INTO precios_hardware (tipo, marca, modelo, precio, fecha_registro)
        VALUES (?, ?, ?, ?, ?)
        """
        datos = (
            componente._tipo,
            componente._marca,
            componente._modelo,
            componente.precio, 
            componente._fecha
        )
        try:
            with self._conectar() as conexion:
                cursor = conexion.cursor()
                cursor.execute(query, datos)
                conexion.commit()
                return True
        except sqlite3.Error as e:
            print(f"[DAO] Error en INSERT: {e}")
            return False

    def obtener_todos(self):
        query = "SELECT * FROM precios_hardware ORDER BY id DESC"
        try:
            with self._conectar() as conexion:
                cursor = conexion.cursor()
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[DAO] Error en SELECT: {e}")
            return []