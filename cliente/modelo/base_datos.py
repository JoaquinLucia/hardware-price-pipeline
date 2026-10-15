# cliente/modelo/base_datos.py

import sqlite3
from .observador import Sujeto

class GestorBaseDatos(Sujeto):
    def __init__(self, nombre_db="hardware_pipeline.db"):
        # Inicializamos el constructor
        super().__init__()
        self.nombre_db = nombre_db
        self._crear_tabla()

    def _conectar(self):
        #Conecta a sqlite
        return sqlite3.connect(self.nombre_db)

    def _crear_tabla(self):
        #Crea la tabla si no existe
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
            print(f"Error al inicializar la base de datos: {e}")

    def registrar_precio(self, componente):
        """
        Inserta un nuevo registro en la base de datos y
        notifica a los observadores sobre el resultado.
        """
        query = """
        INSERT INTO precios_hardware (tipo, marca, modelo, precio, fecha_registro)
        VALUES (?, ?, ?, ?, ?)
        """
        # Se asume que 'componente' es una instancia de tu clase POO
        datos = (
            componente._tipo,
            componente._marca,
            componente._modelo,
            componente.precio,  # Usando el @property
            componente._fecha
        )

        try:
            with self._conectar() as conexion:
                cursor = conexion.cursor()
                cursor.execute(query, datos)
                conexion.commit()

                # ¡ACÁ APLICAMOS EL PATRÓN OBSERVADOR!
                # Si el INSERT fue exitoso, notificamos el evento.
                mensaje_log = f"INSERT OK: {componente._marca} {componente._modelo} a ${componente.precio}"
                self.notificar("NUEVO_REGISTRO", mensaje_log)
                
                return True

        except sqlite3.Error as e:
            # Si falla la base de datos, también notificamos el error para que quede registrado
            mensaje_error = f"ERROR SQLite al registrar {componente._modelo}: {e}"
            self.notificar("ERROR_BD", mensaje_error)
            return False

    def obtener_historial(self):
        """Recupera todos los registros para la Vista."""
        query = "SELECT * FROM precios_hardware ORDER BY id DESC"
        try:
            with self._conectar() as conexion:
                cursor = conexion.cursor()
                return cursor.fetchall()
        except sqlite3.Error as e:
            self.notificar("ERROR_BD", f"Error al leer historial: {e}")
            return []