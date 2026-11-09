from app.dao.conexion import obtener_conexion
from app.modelo.precio import PrecioHistorico

class PrecioDAO:
    
    @staticmethod
    def guardar(id_producto, monto):  # <-- Acá está la clave: recibe los dos
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            # Insertamos ambos valores. La fecha la pone SQLite sola con 'now'
            cursor.execute('''
                INSERT INTO historial_precios (id_producto, monto, fecha) 
                VALUES (?, ?, datetime('now', 'localtime'))
            ''', (id_producto, monto))
            conn.commit()
    @staticmethod
    def obtener_historial(id_producto):
        """
        Devuelve una lista de objetos PrecioHistorico ordenados cronológicamente.
        """
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, id_producto, monto, fecha 
                FROM historial_precios 
                WHERE id_producto = ? 
                ORDER BY fecha ASC
            ''', (id_producto,))
            filas = cursor.fetchall()
            
            historial = []
            for fila in filas:
                precio = PrecioHistorico(
                    id_precio=fila[0], 
                    id_producto=fila[1], 
                    monto=fila[2], 
                    fecha=fila[3]
                )
                historial.append(precio)
                
        return historial