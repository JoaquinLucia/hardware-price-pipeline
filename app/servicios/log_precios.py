import os
from datetime import datetime
from app.servicios.cliente_log import cliente_log_global

DIRECTORIO_LOGS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
ARCHIVO_CAMBIOS = os.path.join(DIRECTORIO_LOGS, 'cambios_precios.txt')

def registrar_cambio_precio(nombre_producto, tienda, precio_viejo, precio_nuevo):
    """
    Escribe la variación de precio en 'cambios_precios.txt' 
    y transmite una alerta por socket TCP asíncrono.
    """
    diferencia = precio_nuevo - precio_viejo
    porcentaje = (diferencia / precio_viejo) * 100
    tipo = "BAJÓ 🔻" if diferencia < 0 else "SUBIÓ 🔺"
    fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 1. Formato de registro en texto plano
    linea = (
        f"[{fecha_hora}] [{tienda}] {nombre_producto} | "
        f"Precio anterior: ${precio_viejo:,.2f} -> Nuevo: ${precio_nuevo:,.2f} "
        f"({tipo} ${abs(diferencia):,.2f} / {porcentaje:+.2f}%)\n"
    )
    
    # 2. Persistencia local en archivo de logs
    os.makedirs(DIRECTORIO_LOGS, exist_ok=True)
    with open(ARCHIVO_CAMBIOS, 'a', encoding='utf-8') as f:
        f.write(linea)
        
    print(f"    [ALERTA PRECIO] {linea.strip()}")
    
    # 3. Transmisión asíncrona hacia el servidor de logs por socket
    mensaje_socket = (
        f"ALERTA PRECIO: {nombre_producto} ({tienda}) cambió de "
        f"${precio_viejo:,.2f} a ${precio_nuevo:,.2f} ({tipo} {porcentaje:+.2f}%)"
    )
    cliente_log_global.enviar_mensaje(mensaje_socket)