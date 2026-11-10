import os
from datetime import datetime

DIRECTORIO_LOGS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app'))
ARCHIVO_CAMBIOS = os.path.join(DIRECTORIO_LOGS, 'cambios_precios.txt')

def registrar_cambio_precio(nombre_producto, tienda, precio_viejo, precio_nuevo):
    """Escribe en un .txt cada vez que detecta una variación de precio."""
    diferencia = precio_nuevo - precio_viejo
    porcentaje = (diferencia / precio_viejo) * 100
    
    # Determinamos el tipo de evento
    if diferencia < 0:
        tipo = "BAJÓ 🔻"
    else:
        tipo = "SUBIÓ 🔺"
        
    fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    linea = (
        f"[{fecha_hora}] [{tienda}] {nombre_producto} | "
        f"Precio anterior: ${precio_viejo:,.2f} -> Nuevo: ${precio_nuevo:,.2f} "
        f"({tipo} ${abs(diferencia):,.2f} / {porcentaje:+.2f}%)\n"
    )
    
    os.makedirs(DIRECTORIO_LOGS, exist_ok=True)
    with open(ARCHIVO_CAMBIOS, 'a', encoding='utf-8') as f:
        f.write(linea)
        
    print(f" [ALERTA PRECIO] {linea.strip()}")