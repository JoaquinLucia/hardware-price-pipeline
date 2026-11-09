import time
from app.servicios.crawler import CrawlerCategorias
from app.servicios.factory import ScraperFactory
from app.dao.producto_dao import ProductoDAO
from app.dao.precio_dao import PrecioDAO
from app.modelo.producto import Producto

def procesar_categoria_entera(url_categoria, nombre_categoria):
    print(f"\n--- INICIANDO INGESTA DE CATEGORÍA: {nombre_categoria.upper()} ---")
    links = CrawlerCategorias.extraer_links(url_categoria)
    total = len(links)
    print(f"Se encontraron {total} productos para procesar.\n")

    for i, link in enumerate(links, 1):
        try:
            print(f"[{i}/{total}] Extrayendo: {link}")
            
            # 1. Scrapeamos el precio y nombre
            scraper = ScraperFactory.obtener_scraper(link)
            datos = scraper.extraer_datos(link)
            
            if datos:
                # 2. Armamos el objeto con la categoría incluida
                nuevo_producto = Producto(
                    nombre=datos['nombre'],
                    url=datos['url'],
                    tienda=datos['tienda'],
                    categoria=nombre_categoria
                )
                
                # 3. Guardamos en SQLite
                id_prod = ProductoDAO.guardar(nuevo_producto)
                PrecioDAO.guardar(id_prod, datos['precio'])
            
            # CLAVE: Pausamos 1.5 segundos entre cada producto para no saturar 
            # el servidor de FullH4rd y evitar que nos baneen la IP
            time.sleep(1.5)
            
        except Exception as e:
            print(f" [X] Error en {link}: {e}")

if __name__ == "__main__":
    # URL de procesadores en FullH4rd
    url_procesadores = "https://www.fullh4rd.com.ar/cat/search/microprocesador"
    
    # Ejecutamos el pipeline
    procesar_categoria_entera(url_procesadores, "Procesadores")
    print("\n--- INGESTA FINALIZADA ---")