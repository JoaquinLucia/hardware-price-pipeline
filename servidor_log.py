import socket
import threading
from datetime import datetime
import os

# Configuración del servidor
HOST = '127.0.0.1'  # Localhost
PUERTO = 9999       # Mismo puerto que configuramos en cliente_log.py
ARCHIVO_LOG = 'registro_auditoria.txt'

def manejar_cliente(conexion, direccion):
    """
    Esta subrutina se ejecuta en un hilo nuevo por cada conexión entrante.
    Recibe el mensaje, le estampa la hora exacta y lo guarda en el txt.
    """
    try:
        # Recibimos hasta 1024 bytes (suficiente para un log)
        datos = conexion.recv(1024)
        if datos:
            mensaje_decodificado = datos.decode('utf-8')
            fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Formateamos la línea del log con marca de tiempo y origen
            linea_log = f"[{fecha_hora}] [IP: {direccion[0]}] {mensaje_decodificado}\n"
            
            # Escribimos en el archivo de texto en modo 'append' (agregar al final)
            with open(ARCHIVO_LOG, 'a', encoding='utf-8') as archivo:
                archivo.write(linea_log)
                
            print(f"Log registrado: {mensaje_decodificado}")
            
    except Exception as e:
        print(f"[ERROR] Hubo un problema al procesar el log del cliente {direccion}: {e}")
    finally:
        # Siempre cerramos la conexión para no dejar puertos colgados
        conexion.close()

def iniciar_servidor():
    """
    Inicia el servidor TCP y se queda escuchando conexiones de forma infinita.
    """
    # Creamos el socket TCP/IP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Asociamos el socket al host y puerto
        servidor.bind((HOST, PUERTO))
        
        # Escuchamos, permitiendo hasta 5 conexiones en cola si hay pico de tráfico
        servidor.listen(5)
        print(f"[*] Servidor de Logs Iniciado y escuchando en {HOST}:{PUERTO}")
        print(f"[*] Los registros se guardarán en: {os.path.abspath(ARCHIVO_LOG)}")
        print("[-] Presiona Ctrl+C para detener el servidor.\n")
        
        # Bucle infinito para mantener el servidor vivo
        while True:
            # accept() bloquea la ejecución hasta que llega un cliente (el controlador/scraper)
            conexion, direccion = servidor.accept()
            
            # Al llegar un log, creamos un Hilo (Thread) para atenderlo y volvemos a escuchar
            hilo = threading.Thread(target=manejar_cliente, args=(conexion, direccion))
            hilo.start()
            
    except KeyboardInterrupt:
        print("\n[*] Apagando el servidor de logs...")
    except Exception as e:
        print(f"[ERROR CRÍTICO] El servidor falló: {e}")
    finally:
        servidor.close()

if __name__ == '__main__':
    iniciar_servidor()