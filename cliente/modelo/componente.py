from datetime import datetime

class ComponenteHardware:
    def __init__(self, tipo, marca, modelo, precio):
        self._tipo = tipo
        self._marca = marca
        self._modelo = modelo
        self._precio = precio
        self._fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = nuevo_precio