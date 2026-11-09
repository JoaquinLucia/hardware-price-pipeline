import sqlite3
import os
import random
from datetime import datetime, timedelta

# Conectamos a la BD usando ruta absoluta
ruta_db = os.path.abspath(os.path.join(os.path.dirname(__file__), 'hardware.db'))

with sqlite3.connect(ruta_db) as conn:
    cursor = conn.cursor()
    
    # Tomamos el precio base del procesador (ID 1)
    precio_base = 358500 
    
    # Inyectamos 7 días de historial hacia atrás
    for dias_atras in range(7, 0, -1):
        fecha_simulada = (datetime.now() - timedelta(days=dias_atras)).strftime("%Y-%m-%d 10:00:00")
        # Simulamos fluctuaciones de precio aleatorias entre -15k y +15k pesos
        precio_simulado = precio_base + random.randint(-15000, 15000)
        
        cursor.execute('''
            INSERT INTO historial_precios (id_producto, monto, fecha) 
            VALUES (?, ?, ?)
        ''', (1, precio_simulado, fecha_simulada))
        
    conn.commit()

print("[EXITO] 7 días de historial simulado inyectados para el ID 1.")