import os
import sys

# Asegurar que el directorio raíz esté en el path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.controlador.controlador_web import app

if __name__ == "__main__":
    print("==================================================")
    print("   MONITOR DE PRECIOS DE HARDWARE - UTN 2026")
    print("==================================================")
    print(" -> Servidor web iniciado en: http://127.0.0.1:5000")
    print(" -> Presioná CTRL+C para detener el servicio.\n")
    
    # Instancia y corre la aplicación Flask completa
    app.run(debug=True, host='127.0.0.1', port=5000)