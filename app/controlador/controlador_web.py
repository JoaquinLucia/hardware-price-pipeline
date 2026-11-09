import os
from flask import Flask, render_template
from app.dao.producto_dao import ProductoDAO

# 1. Calculamos la ruta absoluta exacta donde está este archivo (controlador_web.py)
directorio_base = os.path.abspath(os.path.dirname(__file__))

# 2. Le pegamos la ruta a la carpeta de vistas de forma segura
carpeta_vista = os.path.join(directorio_base, 'app', 'vista')

# 3. Inicializamos Flask pasándole esa ruta blindada
app = Flask(__name__, template_folder=carpeta_vista)
@app.route('/')
def index():
    """
    Ruta principal de la web. 
    1. Le pide los objetos Producto al DAO (Modelo).
    2. Se los envía a index.html (Vista) para que los dibuje.
    """
    lista_productos = ProductoDAO.obtener_todos_los_productos()
    
    return render_template('index.html', productos=lista_productos)

if __name__ == '__main__':
    print("--- INICIANDO SERVIDOR WEB (FLASK) ---")
    # debug=True permite que el servidor se reinicie solo si hacés cambios en el código
    app.run(debug=True, port=5000)