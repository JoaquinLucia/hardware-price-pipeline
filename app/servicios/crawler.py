import time
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class CrawlerCategorias:
    @staticmethod
    def extraer_links(url_categoria):
        dominio = urlparse(url_categoria).netloc.lower()
        
        # 1. AUTODETECCIÓN DE TIENDA Y CONFIGURACIÓN DINÁMICA
        if 'fullh4rd' in dominio:
            referer_header = 'https://www.fullh4rd.com.ar/'
            # Fullh4rd agrupa los productos bajo la ruta /prod/
            filtro_tienda = lambda href: '/prod/' in href
        elif 'venex' in dominio:
            referer_header = 'https://www.venex.com.ar/'
            # Los productos de Venex son URLs limpias que terminan en .html (sin parámetros ?)
            filtro_tienda = lambda href: href.endswith('.html') and '?' not in href
        else:
            print(f" [Crawler] Dominio no soportado: {dominio}")
            return []

        # 2. SETUP DEL SCRAPER
        scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'es-AR,es;q=0.9,en;q=0.8',
            'Referer': referer_header
        }
        
        links_productos = []
        pagina = 1
        url_base = url_categoria.split('?')[0].rstrip('/')
        
        # 3. ESCANEO Y PAGINACIÓN
        while True:
            # Ambas tiendas suelen usar ?page= para paginar
            url_actual = f"{url_base}?page={pagina}"
            print(f" [Crawler] Escaneando grilla página {pagina} ({url_actual})...")
            
            exito = False
            for intento in range(1, 4):  # Hasta 3 reintentos si salta 403
                try:
                    respuesta = scraper.get(url_actual, headers=headers, timeout=15)
                    
                    if respuesta.status_code == 200:
                        exito = True
                        break
                    elif respuesta.status_code == 403:
                        print(f"     Intento {intento}: 403 detectado. Reintentando en 3s...")
                        time.sleep(3)
                    else:
                        print(f"     HTTP {respuesta.status_code}. Finalizando categoría.")
                        break
                except Exception as e:
                    print(f"     Error de conexión: {e}. Reintentando...")
                    time.sleep(3)
            
            if not exito:
                print(f" [Crawler] No se pudo acceder a la página {pagina}. Fin del escaneo.")
                break
                
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            enlaces = soup.find_all('a', href=True)
            
            nuevos_en_pagina = 0
            for a in enlaces:
                href = a['href']
                
                # 4. APLICAMOS EL FILTRO DINÁMICO DE LA TIENDA
                if filtro_tienda(href):
                    link_absoluto = urljoin(url_categoria, href)
                    dominio_link = urlparse(link_absoluto).netloc.lower()
                    
                    # Verificamos que sea del mismo dominio y no esté duplicado
                    if dominio in dominio_link and link_absoluto not in links_productos:
                        links_productos.append(link_absoluto)
                        nuevos_en_pagina += 1
                        
            print(f"    -> Encontrados {nuevos_en_pagina} productos en la página {pagina}.")
            
            if nuevos_en_pagina == 0:
                print(" [Crawler] Fin de la categoría alcanzado (0 productos nuevos).")
                break
                
            pagina += 1
            time.sleep(1.5)  # Pausa respetuosa para evitar baneos
            
        return links_productos