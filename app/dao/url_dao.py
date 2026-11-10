import sqlite3
from app.dao.conexion import obtener_conexion

class UrlDAO:
    @staticmethod
    def _crear_tabla_si_no_existe():
        """Crea la tabla automáticamente si todavía no fue creada en SQLite."""
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS urls_monitoreadas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL
                )
            ''')
            conn.commit()

    @staticmethod
    def guardar_url(url):
        UrlDAO._crear_tabla_si_no_existe()
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO urls_monitoreadas (url) VALUES (?)", (url,))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    @staticmethod
    def obtener_todas():
        UrlDAO._crear_tabla_si_no_existe()
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT url FROM urls_monitoreadas")
            return [fila[0] for fila in cursor.fetchall()]