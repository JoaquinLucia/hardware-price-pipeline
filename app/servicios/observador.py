from abc import ABC, abstractmethod
from app.servicios.cliente_log import cliente_log_global

class Observador(ABC):
    @abstractmethod
    def actualizar(self, evento, mensaje):
        pass

class ObservadorConsola(Observador):
    def actualizar(self, evento, mensaje):
        print(f"[{evento.upper()}] {mensaje}")

class ObservadorSocket(Observador):
    def actualizar(self, evento, mensaje):
        mensaje_formateado = f"[{evento.upper()}] {mensaje}"
        cliente_log_global.enviar_mensaje(mensaje_formateado)

class GestorLogs:
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

gestor_logs_global = GestorLogs()
gestor_logs_global.adjuntar(ObservadorConsola())
gestor_logs_global.adjuntar(ObservadorSocket())