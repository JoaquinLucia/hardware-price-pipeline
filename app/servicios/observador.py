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

# --- EL SUJETO ---
class GestorLogs:
    """
    Actúa como un Singleton o instancia global a la que los decoradores
    le avisan cuando pasa algo.
    """
    _instancia = None

    def __new__(cls):
        # Implementación simple de Singleton para usar el mismo gestor en toda la app
        if cls._instancia is None:
            cls._instancia = super(GestorLogs, cls).__new__(cls)
            cls._instancia.observadores = []
        return cls._instancia

    def adjuntar(self, observador: Observador):
        if observador not in self.observadores:
            self.observadores.append(observador)

    def desvincular(self, observador: Observador):
        self.observadores.remove(observador)

    def notificar(self, evento, mensaje):
        for observador in self.observadores:
            observador.actualizar(evento, mensaje)

# Instancia global para ser usada por el decorador
gestor_logs_global = GestorLogs()