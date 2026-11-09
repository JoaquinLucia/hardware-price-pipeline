import os
from flask import Flask, render_template
from app.dao.producto_dao import ProductoDAO
from app.dao.precio_dao import PrecioDAO
from flask import Flask, render_template, request, redirect  
from app.dao.url_dao import UrlDAO          
from app.modelo.producto import Producto        
from app.servicios.factory import ScraperFactory        

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
    print(f"[SISTEMA] Flask encontró {len(lista_productos)} productos en la BD.")
    datos_vista = []
    for producto in lista_productos:
        historial = PrecioDAO.obtener_historial(producto.id)
        
        # Si hay historial, tomamos el monto del último registro (índice -1)
        precio_actual = historial[-1].monto if historial else 0
        
        datos_vista.append({
            "producto": producto,
            "precio_actual": precio_actual
        })
    
    return render_template('index.html', datos=datos_vista)

@app.route('/producto/<int:id_producto>')
def detalle_producto(id_producto):
    """
    Ruta de detalle: Busca el producto, su historial, y envía los datos
    preparados para alimentar el gráfico de Chart.js.
    """
    producto = ProductoDAO.obtener_por_id(id_producto)
    historial = PrecioDAO.obtener_historial(id_producto)
    
    if not producto:
        return "Producto no encontrado", 404
        
    # Extraemos fechas y precios en listas separadas para el gráfico
    # Usamos rebanado en la fecha para sacar los milisegundos si los hay (ej: '2026-11-06 15:30')
    fechas_grafico = [h.fecha[:16] for h in historial] 
    precios_grafico = [h.monto for h in historial]
    
    return render_template(
        'detalle_producto.html', 
        producto=producto, 
        fechas=fechas_grafico, 
        precios=precios_grafico
    )

@app.route('/agregar_url', methods=['POST'])
def agregar_url():
    """
    Panel Admin: Recibe la URL, ejecuta el scraper en caliente,
    guarda el producto y su precio actual, y actualiza la vista.
    """
    nueva_url = request.form.get('url_input')
    
    if nueva_url:
        try:
            # 1. Scraper
            scraper = ScraperFactory.obtener_scraper(nueva_url)
            datos = scraper.extraer_datos(nueva_url)
            
            if datos:
                print(f"[DEBUG 1] Precio extraído crudo: {datos['precio']}")
                
                # 2. Guardar Producto
                nuevo_producto = Producto(
                    nombre=datos['nombre'],
                    url=datos['url'],
                    tienda=datos['tienda']
                )
                id_generado = ProductoDAO.guardar(nuevo_producto)
                print(f"[DEBUG 2] Producto guardado en BD con ID: {id_generado}")
                
                # 3. Guardar Precio
                PrecioDAO.guardar(id_generado, datos['precio'])
                print(f"[DEBUG 3] Historial de precio guardado exitosamente.")
                
        except Exception as e:
            print(f"[ERROR EN PANEL ADMIN] Detalle del fallo: {e}")
            
    return redirect('/')

if __name__ == '__main__':
    print("--- INICIANDO SERVIDOR WEB (FLASK) ---")
    # debug=True permite que el servidor se reinicie solo si hacés cambios en el código
    app.run(debug=True, port=5000)