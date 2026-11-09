import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class CrawlerCategorias:
    @staticmethod
    def extraer_links(url_categoria):
        """
        Descarga la página de una categoría evadiendo firewalls (Cloudflare), 
        y devuelve una lista limpia con las URLs de los productos.
        """
        dominio = urlparse(url_categoria).netloc.lower()
        
        # Creamos el scraper que simula un navegador humano al 100%
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
        
        try:
            respuesta = scraper.get(url_categoria, timeout=15)
            respuesta.raise_for_status()
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            
            links_productos = []
            
            if 'venex.com.ar' in dominio:
                # Venex suele agrupar los productos en divs con clase 'product-box'
                cajas = soup.select('.product-box h3 a, .product-box-c h3 a')
                for a in cajas:
                    link_absoluto = urljoin('https://www.venex.com.ar', a['href'])
                    if link_absoluto not in links_productos:
                        links_productos.append(link_absoluto)
                        
            elif 'fullh4rd.com.ar' in dominio:
                # FullH4rd usa clases 'item' o 'info'
                cajas = soup.select('.item .info h3 a, .item a')
                for a in cajas:
                    link_absoluto = urljoin('https://www.fullh4rd.com.ar', a['href'])
                    if link_absoluto not in links_productos:
                        links_productos.append(link_absoluto)
            else:
                raise ValueError(f"Crawler no soportado para el dominio: {dominio}")
                
            return links_productos
            
        except Exception as e:
            print(f"[ERROR CRAWLER] No se pudo acceder a la categoría: {e}")
            return []