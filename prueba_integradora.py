from app.dao.conexion import inicializar_base_de_datos
from app.servicios.factory import ScraperFactory
from app.servicios.observador import gestor_logs_global, ObservadorConsola, ObservadorSocket
from app.modelo.producto import Producto
from app.modelo.precio import PrecioHistorico
from app.dao.producto_dao import ProductoDAO
from app.dao.precio_dao import PrecioDAO


def ejecutar_prueba():
    print("--- INICIANDO INTEGRACIÓN ETL (SCRAPER + DAO + LOGS) ---")
    
    # 1. Preparar la Base de Datos (crea hardware.db y las tablas si no existen)
    inicializar_base_de_datos()
    print("[SISTEMA] Base de datos SQLite lista.")

    # 2. Configurar el Patrón Observador para que el decorador envíe logs
    gestor_logs_global.adjuntar(ObservadorConsola())
    gestor_logs_global.adjuntar(ObservadorSocket())
    
    # URL real de prueba de Venex (podés cambiarla por cualquier componente)
    # Por ejemplo, busquemos un Ryzen 5 3600 (tu procesador actual) o similar
    url_prueba = "https://fullh4rd.com.ar/prod/33250/placa-de-video-geforce-g210-1gb-arktek-cyclops"
    
    try:
        # 3. EXTRAER (Extract - Scraper)
        print("\n--- FASE 1: EXTRACCIÓN ---")
        scraper = ScraperFactory.obtener_scraper(url_prueba)
        # Esto disparará los decoradores y mandará los logs por TCP automáticamente
        datos = scraper.extraer_datos(url_prueba)
        
        print(f"Datos obtenidos crudos: {datos}")
        
        # 4. TRANSFORMAR Y CARGAR (Transform & Load - Modelos y DAO)
        print("\n--- FASE 2: CARGA EN BASE DE DATOS ---")
        
        # Armamos el objeto puro Producto
        producto_nuevo = Producto(
            nombre=datos['nombre'], 
            url=datos['url'], 
            tienda=datos['tienda']
        )
        
        # El DAO lo guarda o recupera su ID si ya existía
        producto_bd = ProductoDAO.guardar(producto_nuevo)
        print(f"Producto gestionado en BD con ID: {producto_bd.id}")
        
        # Armamos el objeto puro PrecioHistorico enlazándolo al ID del producto
        precio_nuevo = PrecioHistorico(
            id_producto=producto_bd.id, 
            monto=datos['precio']
        )
        
        # El DAO inserta el registro histórico
        precio_bd = PrecioDAO.guardar(precio_nuevo)
        print(f"Precio de ${precio_bd.monto} registrado exitosamente bajo el historial ID: {precio_bd.id}")

        print("\n--- INTEGRACIÓN FINALIZADA CON ÉXITO ---")

    except Exception as e:
        print(f"\n[ERROR DE INTEGRACIÓN] Falló el proceso: {e}")
        gestor_logs_global.notificar("ERROR", f"Fallo en prueba integradora: {e}")

if __name__ == '__main__':
    ejecutar_prueba()