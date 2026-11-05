import socket
import threading
from datetime import datetime

class ServidorLogsSocket:
    def __init__(self, host="127.0.0.1", puerto=9999):
        self.host = host
        self.puerto = puerto
        self.ejecutando = False

    def iniciar(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((self.host, self.puerto))
        servidor.listen(5)
        self.ejecutando = True
        print(f"[SERVIDOR SOCKET] Escuchando en {self.host}:{self.puerto}...")

        try:
            while self.ejecutando:
                socket_cliente, direccion = servidor.accept()
                hilo = threading.Thread(
                    target=self._manejar_cliente, 
                    args=(socket_cliente, direccion), 
                    daemon=True
                )
                hilo.start()
        except KeyboardInterrupt:
            print("\n[SERVIDOR SOCKET] Apagando servidor...")
        finally:
            servidor.close()

    def _manejar_cliente(self, socket_cliente, direccion):
        with socket_cliente:
            mensaje = socket_cliente.recv(1024).decode("utf-8")
            if mensaje:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                registro = f"[{timestamp}] [{direccion[0]}] {mensaje}\n"
                print(f"[LOG RECIBIDO] {registro.strip()}")
                with open("log_servidor.txt", "a", encoding="utf-8") as f:
                    f.write(registro)

if __name__ == "__main__":
    servidor = ServidorLogsSocket()
    servidor.iniciar()