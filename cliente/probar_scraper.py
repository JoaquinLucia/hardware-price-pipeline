from modelo.gestor_precios import GestorPrecios
from modelo.observador_socket import ObservadorSocket
from scraper.scraper_hardware import ScraperVenex

def probar():
    # 1. Inicializamos modelo y observador socket
    gestor = GestorPrecios()
    observador_socket = ObservadorSocket()
    gestor.agregar_observador(observador_socket)

    # 2. Instanciamos el scraper
    scraper = ScraperVenex(gestor)

    # 3. Probamos con una URL real de Venex
    url_prueba = "https://www.venex.com.ar/componentes-de-pc/microprocesadores/microprocesador-amd-ryzen-7-5700x-8-16-4-6ghz-s-g-s-cooler-zen3.html"
    
    print("Iniciando prueba del scraper...")
    scraper.scrapear_producto_individual(url_prueba, "Procesador")

if __name__ == "__main__":
    probar()