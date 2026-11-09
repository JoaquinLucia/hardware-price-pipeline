import socket
import time

def enviar_log_prueba(mensaje, host='127.0.0.1', puerto=9999):
    """
    Simula la acción que hará ClienteSocketLog.
    Abre una conexión, manda el texto y cierra.
    """
    print(f"Enviando: {mensaje}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, puerto))
            s.sendall(mensaje.encode('utf-8'))
        print("-> Enviado con éxito.")
    except ConnectionRefusedError:
        print("-> [ERROR] No se pudo conectar. ¿Está corriendo servidor_log.py?")
    except Exception as e:
        print(f"-> [ERROR INESPERADO]: {e}")

if __name__ == '__main__':
    print("--- INICIANDO PRUEBA DE CONEXIÓN TCP ---")
    
    # 1. Simulamos el inicio de un scraper
    enviar_log_prueba("[INFO] Iniciando ejecución de 'extraer_datos_venex'...")
    time.sleep(1) # Pausa breve para simular tiempo de proceso
    
    # 2. Simulamos un scraping exitoso
    enviar_log_prueba("[EXITO] 'extraer_datos_venex' finalizó correctamente en 1.45 segundos.")
    time.sleep(1)
    
    # 3. Simulamos una caída de red en otra tienda
    enviar_log_prueba("[ERROR] Fallo en 'extraer_datos_compragamer': HTTPSConnectionPool (Timeout)")
    
    print("--- PRUEBA FINALIZADA ---")
    print("Revisá la consola del servidor_log.py y el archivo registro_auditoria.txt")