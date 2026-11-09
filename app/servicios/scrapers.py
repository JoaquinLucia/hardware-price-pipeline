from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import re
from app.servicios.decoradores import registro_log_scraper

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

    def extraer_datos(self, url):
        html_crudo = self.hacer_peticion(url)
        soup = BeautifulSoup(html_crudo, 'html.parser')
        
        try:
            # --- 1. BUSCAR NOMBRE (Técnica OpenGraph / Redes Sociales) ---
            meta_og_title = soup.find('meta', property='og:title')
            
            if not meta_og_title or not meta_og_title.get('content'):
                raise ValueError("No se encontró el meta tag og:title con el nombre del producto.")
                
            nombre_crudo = meta_og_title['content'].strip()
            
            # Limpiamos por si le agregan " | Venex" al final en la metadata
            nombre_producto = nombre_crudo.split('|')[0].split('- Venex')[0].strip()
            # 2. Buscar Precio
            etiqueta_precio = soup.find(class_=re.compile(r'price', re.IGNORECASE))
            if not etiqueta_precio:
                raise ValueError("No se encontró la etiqueta del precio.")
                
            precio_texto = etiqueta_precio.text.strip()
            
            # --- FASE DE TRANSFORMACIÓN (ETL) ---
            # 1. Quitamos símbolos de moneda y ajustamos los decimales
            precio_limpio = precio_texto.replace('$', '').replace('.', '').replace(',', '.').strip()
            
            # 2. Dividimos el bloque gigante de texto usando los espacios/saltos de línea
            # split() por defecto corta en cada espacio o \n. Nos quedamos con el índice [0]
            primer_valor = precio_limpio.split()[0]
            
            # 3. Ahora sí, convertimos el número puro a float
            precio_float = float(primer_valor)
            
            return {
                "nombre": nombre_producto,
                "precio": precio_float,
                "url": url,
                "tienda": self.nombre_tienda
            }
            
        except Exception as e:
            # TÁCTICA DE DEBUGGING: Guardamos el HTML crudo
            with open("debug_venex.html", "w", encoding="utf-8") as f:
                f.write(html_crudo)
            
            raise ValueError(f"Fallo en la extracción. Se generó 'debug_venex.html' para revisar. Detalle: {e}")


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