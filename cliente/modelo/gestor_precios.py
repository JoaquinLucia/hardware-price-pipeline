from .observador import Sujeto
from persistencia.dao import HardwareDAO

class GestorPrecios(Sujeto):
    """
    Capa de servicio y lógica de negocio.
    Hereda de Sujeto para aplicar el Patrón Observador.
    """
    def __init__(self):
        super().__init__()
        # Instanciamos el DAO por composición
        self.dao = HardwareDAO()

    def registrar_nuevo_precio(self, componente):
        """
        Intenta guardar mediante el DAO y notifica a los observadores
        del resultado (ideal para enviar al Socket).
        """
        exito = self.dao.insertar(componente)
        
        if exito:
            mensaje_log = f"OK: Registrado {componente._marca} {componente._modelo} | Precio: ${componente.precio}"
            self.notificar("NUEVO_REGISTRO", mensaje_log)
            return True
        else:
            self.notificar("ERROR_BD", f"Fallo al registrar {componente._modelo}")
            return False

    def obtener_historial(self):
        return self.dao.obtener_todos()