import sqlite3
import os
from app.modelo.producto import Producto

def obtener_conexion():
    """Establece y devuelve la conexión a la base de datos SQLite."""
    ruta_db = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'hardware.db'))
    return sqlite3.connect(ruta_db)

class ProductoDAO:
    @staticmethod
    def guardar(producto):
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO productos (nombre, url, tienda, categoria) 
                VALUES (?, ?, ?, ?)
            ''', (producto.nombre, producto.url, producto.tienda, producto.categoria))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def obtener_todos_los_productos():
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, url, tienda, categoria FROM productos")
            return [
                Producto(nombre=f[1], url=f[2], tienda=f[3], categoria=f[4], id_producto=f[0])
                for f in cursor.fetchall()
            ]

    @staticmethod
    def obtener_por_id(id_producto):
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, url, tienda, categoria FROM productos WHERE id = ?", (id_producto,))
            fila = cursor.fetchone()
            if fila:
                return Producto(nombre=fila[1], url=fila[2], tienda=fila[3], categoria=fila[4], id_producto=fila[0])
            return None

    @staticmethod
    def obtener_por_categoria(categoria):
        """Método nuevo para los futuros filtros de la interfaz web."""
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, url, tienda, categoria FROM productos WHERE categoria = ?", (categoria,))
            return [
                Producto(nombre=f[1], url=f[2], tienda=f[3], categoria=f[4], id_producto=f[0])
                for f in cursor.fetchall()
            ]