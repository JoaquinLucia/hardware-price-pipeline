import socket

class ClienteSocketLog:
    def __init__(self, host='127.0.0.1', puerto=9999):
        self.host = host
        self.puerto = puerto

    def enviar_mensaje(self, mensaje):
        """
        Abre una conexión TCP, manda el string codificado y cierra.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.puerto))
                s.sendall(mensaje.encode('utf-8'))
        except ConnectionRefusedError:
            # Si el servidor no está corriendo, continuamos sin bloquear
            pass
        except Exception as e:
            print(f"[ERROR SOCKET] {e}")