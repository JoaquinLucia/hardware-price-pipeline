from urllib.parse import urlparse
from app.servicios.scrapers import ScraperVenex, ScraperFullH4rd

class ScraperFactory:
    
    @staticmethod
    def obtener_scraper(url):
        dominio = urlparse(url).netloc.lower()
        
        if 'venex.com.ar' in dominio:
            return ScraperVenex()
            
        # CompraGamer comentado para el futuro
        # elif 'compragamer.com' in dominio:
        #     return ScraperCompraGamer()
            
        elif 'fullh4rd.com.ar' in dominio:
            return ScraperFullH4rd() # <- ¡Activado!
            
        else:
            raise ValueError(f"Sistema no soportado: No existe un scraper para el dominio '{dominio}'.")