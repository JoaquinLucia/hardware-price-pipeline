# cliente/modelo/observador.py

class Sujeto:
    """Clase base para el objeto que será observado."""
    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador):
        if observador not in self._observadores:
            self._observadores.append(observador)

    def quitar_observador(self, observador):
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar(self, evento, detalle):
        """Notifica a todos los observadores registrados."""
        for observador in self._observadores:
            observador.actualizar(evento, detalle)

class Observador:
    """Clase abstracta para los observadores."""
    def actualizar(self, evento, detalle):
        raise NotImplementedError("El método 'actualizar' debe ser implementado por la subclase.")