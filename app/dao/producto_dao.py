import sqlite3
from app.dao.conexion import obtener_conexion
from app.modelo.producto import Producto

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
    def obtener_por_url(url):
        """Busca y devuelve un producto según su URL única."""
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, url, tienda, categoria FROM productos WHERE url = ?", (url,))
            fila = cursor.fetchone()
            if fila:
                return Producto(nombre=fila[1], url=fila[2], tienda=fila[3], categoria=fila[4], id_producto=fila[0])
            return None
        
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
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, url, tienda, categoria FROM productos WHERE categoria = ?", (categoria,))
            return [
                Producto(nombre=f[1], url=f[2], tienda=f[3], categoria=f[4], id_producto=f[0])
                for f in cursor.fetchall()
            ]

    @staticmethod
    def obtener_categorias_existentes():
        """Devuelve una lista con los nombres de todas las categorías cargadas en SQLite."""
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT categoria 
                FROM productos 
                WHERE categoria IS NOT NULL AND categoria != '' 
                ORDER BY categoria ASC
            """)
            filas = cursor.fetchall()
        return [f[0] for f in filas]