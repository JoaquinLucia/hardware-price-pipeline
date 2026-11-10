from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import re
from app.servicios.decoradores import registro_log_scraper
import cloudscraper
from app.dao.conexion import obtener_conexion

# --- CLASE BASE ---
class ScraperHardware(ABC):
    
    def __init__(self, nombre_tienda):
        self.nombre_tienda = nombre_tienda

    @abstractmethod
    def extraer_datos(self, url):
        pass
    
    @registro_log_scraper
    def hacer_peticion(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        respuesta = requests.get(url, headers=headers, timeout=10)
        respuesta.raise_for_status() 
        return respuesta.text

# --- CLASE HIJA (VENEX) ---
class ScraperVenex(ScraperHardware):
    
    def __init__(self):
        super().__init__("Venex")
        # Instanciamos cloudscraper para esquivar las restricciones anti-bot de Venex
        self.scraper_http = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )

    def extraer_datos(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Referer': 'https://www.venex.com.ar/'
        }
        
        try:
            respuesta = self.scraper_http.get(url, headers=headers, timeout=15)
            if respuesta.status_code != 200:
                raise ValueError(f"Error HTTP {respuesta.status_code}")
            html_crudo = respuesta.text
        except Exception as e:
            raise ValueError(f"No se pudo realizar la petición HTTP. Detalle: {e}")

        soup = BeautifulSoup(html_crudo, 'html.parser')
        
        try:
            # --- 1. BUSCAR NOMBRE DESDE LA URL (Más seguro y limpio) ---
            # Separamos por '/' y agarramos la última parte, sacamos el '.html' y cambiamos guiones por espacios
        # Limpiamos primero parámetros de búsqueda y barras finales
            url_limpia = url.split('?')[0].rstrip('/')
            slug = url_limpia.split('/')[-1].replace('.html', '')
            nombre_producto = slug.replace('-', ' ').title()
            
            # --- 2. BUSCAR PRECIO ---
            precio_tag = soup.find(class_='textPrecio')
            if not precio_tag:
                raise ValueError("No se encontró la clase 'textPrecio'.")
                
            precio_texto = precio_tag.text.strip()
            
            # Validamos que al menos contenga números
            if not any(c.isdigit() for c in precio_texto):
                raise ValueError("La etiqueta de precio no contiene valores numéricos.")
            
            # --- FASE DE TRANSFORMACIÓN (ETL) ---
            precio_limpio = precio_texto.replace('$', '').replace('.', '').replace(',', '.').strip()
            
            coincidencia = re.search(r'\d+(\.\d+)?', precio_limpio)
            if not coincidencia:
                raise ValueError(f"No se pudo extraer un número del texto: {precio_texto}")
                
            precio_float = float(coincidencia.group())
            
            return {
                "nombre": nombre_producto,
                "precio": precio_float,
                "url": url,
                "tienda": self.nombre_tienda
            }
            
        except Exception as e:
            # TÁCTICA DE DEBUGGING (Igual a FullH4rd)
            with open("debug_venex.html", "w", encoding="utf-8") as f:
                f.write(html_crudo)
                
            raise ValueError(f"Fallo en la extracción de Venex. Se generó 'debug_venex.html'. Detalle: {e}")


        # --- CLASE HIJA (COMPRAGAMER) ---
class ScraperCompraGamer(ScraperHardware):
    
    def __init__(self):
        super().__init__("CompraGamer")

    def extraer_datos(self, url):
        html_crudo = self.hacer_peticion(url)
        soup = BeautifulSoup(html_crudo, 'html.parser')
        
        try:
            # --- 1. BUSCAR NOMBRE ---
            # Intentamos primero con la metadata de OpenGraph
            meta_og_title = soup.find('meta', property='og:title')
            
            if meta_og_title and meta_og_title.get('content'):
                nombre_crudo = meta_og_title['content'].strip()
            elif soup.title:
                nombre_crudo = soup.title.text.strip()
            else:
                raise ValueError("No se encontró el título ni el og:title.")
            
            # Limpiamos el nombre (CG suele agregar " | Compra Gamer" al final)
            nombre_producto = nombre_crudo.split('|')[0].replace('Compra Gamer', '').strip()
            
            # --- 2. BUSCAR PRECIO ---
            # CG usa clases dinámicas. Buscamos cualquier etiqueta que mencione precio y tenga un $
            etiqueta_precio = soup.find(string=re.compile(r'\$'))
            
            if not etiqueta_precio:
                # Búsqueda alternativa por clase
                etiquetas_candidatas = soup.find_all(class_=re.compile(r'price|precio|monto', re.IGNORECASE))
                for etiqueta in etiquetas_candidatas:
                    if '$' in etiqueta.text:
                        etiqueta_precio = etiqueta.text
                        break
            
            if not etiqueta_precio:
                raise ValueError("No se encontró el precio en el HTML de CompraGamer.")
            
            precio_texto = etiqueta_precio.strip()
            
            # --- FASE DE TRANSFORMACIÓN (ETL) ---
            # Limpieza exhaustiva para CompraGamer
            precio_limpio = precio_texto.replace('$', '').replace('.', '').replace(',', '.').strip()
            primer_valor = precio_limpio.split()[0]
            precio_float = float(primer_valor)
            
            return {
                "nombre": nombre_producto,
                "precio": precio_float,
                "url": url,
                "tienda": self.nombre_tienda
            }
            
        except Exception as e:
            # TÁCTICA DE DEBUGGING
            with open("debug_compragamer.html", "w", encoding="utf-8") as f:
                f.write(html_crudo)
            
            raise ValueError(f"Fallo en la extracción. Se generó 'debug_compragamer.html'. Detalle: {e}")


        # --- CLASE HIJA (FULLH4RD) ---
class ScraperFullH4rd(ScraperHardware):
    
    def __init__(self):
        super().__init__("FullH4rd")

    def extraer_datos(self, url):
        html_crudo = self.hacer_peticion(url)
        soup = BeautifulSoup(html_crudo, 'html.parser')
        
        try:
            # --- 1. BUSCAR NOMBRE ---
            # FullH4rd suele tener un <title> bastante limpio
            if not soup.title:
                raise ValueError("No se encontró la etiqueta <title>.")
                
            nombre_crudo = soup.title.text.strip()
            # Limpiamos la marca de la tienda al final del título
            nombre_producto = nombre_crudo.split('|')[0].replace('FullH4rd', '').replace('FULLH4RD', '').strip()
            
            # --- 2. BUSCAR PRECIO (Reforzado) ---
            etiquetas_candidatas = soup.find_all(class_=re.compile(r'price|precio', re.IGNORECASE))
            
            precio_texto = None
            for etiqueta in etiquetas_candidatas:
                texto = etiqueta.text.strip()
                # Validamos que el texto contenga el símbolo $ y algún número
                if '$' in texto and any(c.isdigit() for c in texto):
                    precio_texto = texto
                    break
                    
            if not precio_texto:
                raise ValueError("No se encontró la etiqueta con el valor numérico del precio.")
            
            # --- FASE DE TRANSFORMACIÓN (ETL) ---
            # Limpieza básica
            precio_limpio = precio_texto.replace('$', '').replace('.', '').replace(',', '.').strip()
            
            # Nos aseguramos de extraer solo la parte numérica usando expresiones regulares,
            # por si la tienda pega letras al número (ej: "350000Especial")
            coincidencia = re.search(r'\d+(\.\d+)?', precio_limpio)
            if not coincidencia:
                raise ValueError(f"No se pudo extraer un número del texto: {precio_limpio}")
                
            precio_float = float(coincidencia.group())
            
            return {
                "nombre": nombre_producto,
                "precio": precio_float,
                "url": url,
                "tienda": self.nombre_tienda
            }
            
        except Exception as e:
            # TÁCTICA DE DEBUGGING
            with open("debug_fullh4rd.html", "w", encoding="utf-8") as f:
                f.write(html_crudo)
            
            raise ValueError(f"Fallo en la extracción. Se generó 'debug_fullh4rd.html'. Detalle: {e}")