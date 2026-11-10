import os
import threading
from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
from app.dao.producto_dao import ProductoDAO
from app.dao.precio_dao import PrecioDAO
from app.dao.url_dao import UrlDAO          
from app.modelo.producto import Producto        
from app.servicios.factory import ScraperFactory  
from app.servicios.actualizador_lotes import ejecutar_actualizacion_completa

# Ruta de la carpeta actual
directorio_base = os.path.abspath(os.path.dirname(__file__))

# ruta de carpeta vista
carpeta_vista = os.path.join(directorio_base, '..', 'vista')

# Inicializamos Flask
app = Flask(__name__, template_folder=carpeta_vista)
app.secret_key = 'clave_secreta_para_mensajes_flash'

@app.route('/')
@app.route('/categoria/<path:nombre_cat>')
def index(nombre_cat="Todas"):
    busqueda = request.args.get('q', '').strip()
    orden = request.args.get('orden', 'asc')

    if nombre_cat == "Todas":
        lista_productos = ProductoDAO.obtener_todos_los_productos()
    else:
        lista_productos = ProductoDAO.obtener_por_categoria(nombre_cat)
    
    datos_vista = []
    for producto in lista_productos:
        if busqueda and busqueda.lower() not in producto.nombre.lower():
            continue

        historial = PrecioDAO.obtener_historial(producto.id)
        precio_actual = historial[-1].monto if historial else 0
        
        datos_vista.append({
            "producto": producto,
            "precio_actual": precio_actual
        })

    if orden == 'desc':
        datos_vista.sort(key=lambda x: x['precio_actual'], reverse=True)
    else:
        datos_vista.sort(key=lambda x: x['precio_actual'])

    categorias_disponibles = ["Todas"] + ProductoDAO.obtener_categorias_existentes()

    # Le pasamos a la vista si hay algún mensaje flash (ej: "Crawler iniciado")
    return render_template(
        'index.html', 
        datos=datos_vista, 
        categoria_actual=nombre_cat,
        busqueda_actual=busqueda,
        orden_actual=orden,
        categorias=categorias_disponibles
    )

@app.route('/producto/<int:id_prod>')
def detalle_producto(id_prod):
    producto = ProductoDAO.obtener_por_id(id_prod)
    if not producto:
        return "Producto no encontrado", 404
        
    historial = PrecioDAO.obtener_historial(id_prod)

    fechas = []
    precios = []
    
    for registro in historial:
        fecha_texto = str(registro.fecha)[:10] 
        try:
            dt = datetime.strptime(fecha_texto, '%Y-%m-%d')
            fechas.append(dt.strftime('%d/%m/%Y'))
        except ValueError:
            fechas.append(fecha_texto)
        precios.append(registro.monto)

    precio_actual = precios[-1] if precios else 0
    
    return render_template('detalle_producto.html', 
                           producto=producto, 
                           fechas=fechas, 
                           precios=precios,
                           precio_actual=precio_actual)

@app.route('/agregar_url', methods=['POST'])
def agregar_url():
    """ Panel Admin: Recibe 1 URL a mano """
    nueva_url = request.form.get('url_input')
    
    if nueva_url:
        try:
            scraper = ScraperFactory.obtener_scraper(nueva_url)
            datos = scraper.extraer_datos(nueva_url)
            
            if datos:
                prod_existente = ProductoDAO.obtener_por_url(datos['url'])
                if prod_existente:
                    id_generado = prod_existente.id
                else:
                    nuevo_producto = Producto(
                        nombre=datos['nombre'],
                        url=datos['url'],
                        tienda=datos['tienda'],
                        categoria="Varios"
                    )
                    id_generado = ProductoDAO.guardar(nuevo_producto)
                
                PrecioDAO.guardar(id_generado, datos['precio'])
                flash('Producto procesado y guardado correctamente.', 'success')
            else:
                flash('No se pudieron extraer datos de la URL proporcionada.', 'warning')
                
        except Exception as e:
            print(f"[ERROR EN PANEL ADMIN] Detalle del fallo: {e}")
            flash('Error al procesar la URL. Verifique que el enlace sea válido.', 'danger')
            
    return redirect('/')

# --- NUEVO ENDPOINT PARA EL CRAWLER ---
@app.route('/ejecutar_crawler', methods=['POST'])
def ejecutar_crawler():
    """
    Inicia la actualización masiva de todas las categorías en un hilo separado (background).
    """
    try:
        # Creamos y arrancamos el hilo para que el escaneo ocurra por detrás
        hilo_scraper = threading.Thread(target=ejecutar_actualizacion_completa)
        hilo_scraper.start()
        
        # En tu index.html podés atajar los flash() para mostrar un cartelito verde
        flash('Actualización masiva iniciada en segundo plano. Esto demorará un rato.', 'success')
    except Exception as e:
        print(f"Error al iniciar hilo: {e}")
        flash('Ocurrió un error al intentar iniciar el scraper.', 'danger')
        
    return redirect('/')

if __name__ == '__main__':
    print("--- INICIANDO SERVIDOR WEB (FLASK) ---")
    app.run(debug=True, port=5000)