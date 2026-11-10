import sqlite3
import os

ruta_db = os.path.abspath(os.path.join(os.path.dirname(__file__), 'hardware.db'))

def unificar_ram():
    if not os.path.exists(ruta_db):
        print(f"No se encontró la base de datos en: {ruta_db}")
        return

    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()
    
    # Reemplazamos las 4 variantes por la categoría unificada "Memorias RAM"
    cursor.execute("""
        UPDATE productos 
        SET categoria = 'Memorias RAM' 
        WHERE categoria IN (
            'Memoria RAM DDR4', 
            'Memoria RAM DDR5', 
            'Memorias RAM (Notebook)', 
            'Memorias RAM (PC)'
        )
    """)
    
    print(f"¡Se unificaron {cursor.rowcount} productos bajo la categoría 'Memorias RAM'!")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    unificar_ram()