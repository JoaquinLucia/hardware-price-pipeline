from .observador import Observador
from utilidades.cliente_socket import enviar_log_al_servidor

class ObservadorSocket(Observador):
    """Observador concreto que retransmite notificaciones al servidor Socket."""
    def actualizar(self, evento, detalle):
        mensaje = f"OBSERVER [{evento}]: {detalle}"
        enviar_log_al_servidor(mensaje)