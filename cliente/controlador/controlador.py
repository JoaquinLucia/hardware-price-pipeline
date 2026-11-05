from modelo.componente import ComponenteHardware
from utilidades.decoradores import decorador_log

class Controlador:
    def __init__(self, modelo):
        self.modelo = modelo
        self.vista = None

    def set_vista(self, vista):
        self.vista = vista

    # ¡Acá está el Punto 3 de tu rúbrica! Decoramos la acción de guardar.
    @decorador_log
    def registrar_ingesta(self, tipo, marca, modelo, precio):
        """Valida los datos de la Vista y los envía al Modelo."""
        try:
            precio_float = float(precio)
            if precio_float < 0:
                return "El precio no puede ser negativo."
            
            # Instanciamos el objeto POO
            componente = ComponenteHardware(tipo, marca, modelo, precio_float)
            
            # El modelo se encarga de guardar y notificar a los observers
            exito = self.modelo.registrar_nuevo_precio(componente)
            
            return "OK" if exito else "Fallo en BD"
            
        except ValueError:
            return "Error: El precio debe ser un número válido."

    def obtener_datos(self):
        """Pide el historial al modelo para mostrarlo en la tabla."""
        return self.modelo.obtener_historial()