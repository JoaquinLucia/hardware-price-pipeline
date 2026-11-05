import socket

def enviar_log_al_servidor(mensaje, host="127.0.0.1", puerto=9999):
    """Envía una cadena de texto al servidor Socket."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.settimeout(2.0)
            cliente.connect((host, puerto))
            cliente.sendall(mensaje.encode("utf-8"))
    except (ConnectionRefusedError, socket.timeout):
        print("[CLIENTE SOCKET] Servidor de logs no disponible.")