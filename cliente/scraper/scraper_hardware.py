import re
import requests
from bs4 import BeautifulSoup
from modelo.componente import ComponenteHardware
from utilidades.decoradores import decorador_log

class ScraperVenex:
    def __init__(self, gestor_precios):
        self.gestor = gestor_precios
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    @decorador_log
    def scrapear_producto_individual(self, url: str, tipo_componente: str):
        print(f"[SCRAPER VENEX] Descargando: {url}...")
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')

# 1. Título: Buscamos todos los h1 y nos quedamos con el más largo
            h1_elements = soup.find_all('h1')
            titulo = None
            if h1_elements:
                textos_h1 = [h1.text.strip() for h1 in h1_elements if h1.text.strip()]
                if textos_h1:
                    titulo = max(textos_h1, key=len) # Agarra el título más largo (el del producto)

            if not titulo:
                print("[SCRAPER ERROR] No se encontró el título del producto.")
                return False    

            # 2. Precio: Extraer importes en formato $ XXX.XXX
            # Buscamos coincidencias con el símbolo $ seguido de cifras con punto
            coincidencias_precio = re.findall(r'\$\s*([\d\.]+)', soup.text)

            precio_final = None
            if coincidencias_precio:
                precios_validos = []
                for p in coincidencias_precio:
                    p_limpio = p.replace('.', '').strip()
                    # Descartamos números chicos (< $1000) para no enganchar cuotas ni meses de garantía
                    if p_limpio.isdigit() and int(p_limpio) > 1000:
                        precios_validos.append(float(p_limpio))

                if precios_validos:
                    # El primer precio válido suele ser el "Precio especial venex" destacado
                    precio_final = precios_validos[0]

            if not precio_final:
                print("[SCRAPER ERROR] No se pudo determinar el precio real.")
                return False

            # 3. Identificar marca automáticamente
            marca = "AMD" if "AMD" in titulo.upper() else ("INTEL" if "INTEL" in titulo.upper() else "NVIDIA" if "NVIDIA" in titulo.upper() else "Genérica")

            # 4. Guardar objeto POO en la base de datos
            componente = ComponenteHardware(
                tipo=tipo_componente,
                marca=marca,
                modelo=titulo,
                precio=precio_final
            )

            exito = self.gestor.registrar_nuevo_precio(componente)
            if exito:
                print(f"[SCRAPER ÉXITO] {titulo} -> ${precio_final}")
                return True

        except Exception as e:
            print(f"[SCRAPER EXCEPCIÓN] Falló al procesar {url}: {e}")
            return False