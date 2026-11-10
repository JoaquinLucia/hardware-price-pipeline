import os
import sys

# 1. Asegurar el directorio raíz en el PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.dao.conexion import inicializar_base_de_datos
from app.controlador.controlador_web import app

if __name__ == "__main__":
    print("==================================================")
    print("   MONITOR DE PRECIOS DE HARDWARE - UTN 2026")
    print("==================================================")
    
    # 2. Verificar e inicializar las tablas en hardware.db
    print(" -> Inicializando base de datos SQLite...")
    inicializar_base_de_datos()
    
    print(" -> Servidor web iniciado en: http://127.0.0.1:5000")
    print(" -> Presioná CTRL+C para detener el servicio.\n")
    
    # 3. Correr la aplicación web
    app.run(debug=True, host='127.0.0.1', port=5000)