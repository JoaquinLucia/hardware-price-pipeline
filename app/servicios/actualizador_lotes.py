import time
from app.dao.producto_dao import ProductoDAO
from app.dao.precio_dao import PrecioDAO
from app.modelo.producto import Producto
from app.servicios.factory import ScraperFactory
from app.servicios.crawler import CrawlerCategorias
from app.servicios.cliente_logs import enviar_log

# Pegamos los diccionarios

categorias_fullh4rd = {
        "Procesadores": ["https://www.fullh4rd.com.ar/microprocesador"],
        "Placa de Video": ["https://fullh4rd.com.ar/tag/placa%20de%20video"],
        "Motherboards": ["https://www.fullh4rd.com.ar/motherboard"],
        "Fuentes": ["https://www.fullh4rd.com.ar/fuentes"],
        "Refrigeracion": ["https://www.fullh4rd.com.ar/refrigeracion"],
        "Gabinetes": ["https://www.fullh4rd.com.ar/gabinetes"],
        "Conectividad y Redes": ["https://www.fullh4rd.com.ar/conectividad-y-redes"],
        "Memorias RAM": [
            "https://fullh4rd.com.ar/tag/memoria%20ram_ddr4",
            "https://fullh4rd.com.ar/tag/memoria%20ram_ddr5",
            "https://fullh4rd.com.ar/tag/ddr4_sodimm",
            "https://fullh4rd.com.ar/tag/ddr5_sodimm"
        ],
        "Discos SATA (HDD)": ["https://fullh4rd.com.ar/almacenamiento/discos-sata"],
        "Discos Externos": ["https://fullh4rd.com.ar/almacenamiento/externos"],
        "Discos SSD": ["https://fullh4rd.com.ar/almacenamiento/discos-ssd"]
    }

categorias_venex = {
        "Procesadores": ["https://www.venex.com.ar/componentes-de-pc/microprocesadores"],
        "Placa de Video": ["https://www.venex.com.ar/componentes-de-pc/placas-de-video"],
        "Motherboards": ["https://www.venex.com.ar/componentes-de-pc/motherboards"],
        "Fuentes": ["https://www.venex.com.ar/componentes-de-pc/fuentes"],
        "Refrigeracion": ["https://www.venex.com.ar/componentes-de-pc/refrigeracion"],
        "Gabinetes": ["https://www.venex.com.ar/componentes-de-pc/gabinetes"],
        "Conectividad y Redes": ["https://www.venex.com.ar/componentes-de-pc/placas-de-red"],
        "Memorias RAM": [
            "https://www.venex.com.ar/componentes-de-pc/memorias-ram/desktop",
         "https://www.venex.com.ar/componentes-de-pc/memorias-ram/notebook"
        ],
        "Discos SATA (HDD)": ["https://www.venex.com.ar/componentes-de-pc/discos-duros-mecanicos"],
        "Discos SSD": ["https://www.venex.com.ar/componentes-de-pc/discos-solidos-ssd"]
    }

def procesar_tienda(diccionario_categorias, nombre_tienda):
    print(f"\n--- INICIANDO ACTUALIZACIÓN MASIVA: {nombre_tienda} ---")
    
    for categoria, lista_urls in diccionario_categorias.items():
        if not lista_urls:
            continue
            
        for url_grilla in lista_urls:
            # todos los links de productos de esta categoría
            links_productos = CrawlerCategorias.extraer_links(url_grilla)
            
            for link in links_productos:
                try:
                    print(f" -> Procesando: {link}")
                    
                    # extraemos datos
                    scraper = ScraperFactory.obtener_scraper(link)
                    datos = scraper.extraer_datos(link)
                    
                    if datos:
                        # persistencia, existe?
                        producto_existente = ProductoDAO.obtener_por_url(link)
                        
                        if producto_existente:
                            id_prod = producto_existente.id
                            print(f"    [OK] Producto existente. ID: {id_prod}")
                        else:
                            # Si no existe, lo creamos asignándole la categoría del diccionario
                            nuevo_producto = Producto(
                                nombre=datos['nombre'],
                                url=datos['url'],
                                tienda=datos['tienda'],
                                categoria=categoria
                            )
                            id_prod = ProductoDAO.guardar(nuevo_producto)
                            print(f"    [NUEVO] Producto creado. ID: {id_prod}")
                            
                        # Guardamos el precio en el historial
                        PrecioDAO.guardar(id_prod, datos['precio'])
                        print(f"    [PRECIO] Historial actualizado: ${datos['precio']}")
                        enviar_log(f"INFO: Producto guardado exitosamente - ID: {id_prod}")
                    
                    time.sleep(1.5) # Pausa entre productos
                    
                except Exception as e:
                    print(f"    [ERROR] Falló el procesamiento de {link}: {e}")
                    enviar_log(f"ERROR: Falló el procesamiento de {link}: {e}")

def ejecutar_actualizacion_completa():
    print("Iniciando tarea programada...")
    procesar_tienda(categorias_venex, "Venex")
    procesar_tienda(categorias_fullh4rd, "Fullh4rd")
    print("--- ACTUALIZACIÓN FINALIZADA CORRECTAMENTE ---")

if __name__ == '__main__':
    ejecutar_actualizacion_completa()