from abc import ABC, abstractmethod
from app.servicios.cliente_log import ClienteSocketLog

# --- LA INTERFAZ DEL OBSERVADOR ---
class Observador(ABC):
    @abstractmethod
    def actualizar(self, evento, mensaje):
        pass

# --- LOS OBSERVADORES CONCRETOS ---
class ObservadorConsola(Observador):
    """Observador básico que imprime en la terminal."""
    def actualizar(self, evento, mensaje):
        print(f"[{evento.upper()}] {mensaje}")

class ObservadorSocket(Observador):
    """Observador que envía el log al servidor externo usando TCP."""
    def __init__(self):
        self.cliente = ClienteSocketLog()
        
    def actualizar(self, evento, mensaje):
        mensaje_formateado = f"[{evento.upper()}] {mensaje}"
        self.cliente.enviar_mensaje(mensaje_formateado)

# --- EL SUJETO (SINGLETON) ---
class GestorLogs:
    """
    Actúa como un Singleton al que los decoradores y servicios le notifican eventos.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GestorLogs, cls).__new__(cls)
            cls._instancia.observadores = []
        return cls._instancia

    def adjuntar(self, observador: Observador):
        if observador not in self.observadores:
            self.observadores.append(observador)

    def desvincular(self, observador: Observador):
        if observador in self.observadores:
            self.observadores.remove(observador)

    def notificar(self, evento, mensaje):
        for observador in self.observadores:
            observador.actualizar(evento, mensaje)

# Instancia global del GestorLogs
gestor_logs_global = GestorLogs()

# --- CONEXIÓN AUTOMÁTICA DE OBSERVADORES ---
gestor_logs_global.adjuntar(ObservadorConsola())
gestor_logs_global.adjuntar(ObservadorSocket())