class Componente:
    def __init__(self, tipo, marca, modelo, precio, fecha_registro):
        self._tipo = tipo       # ej. 'Procesador', 'Monitor'
        self._marca = marca     # ej. 'AMD', 'LG'
        self._modelo = modelo   # ej. 'Ryzen 5 3600', '34 ultrawide'
        self._precio = precio
        self._fecha = fecha_registro

    # Aquí usaríamos properties (Modulo 1, Unidad 2)
    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = nuevo_precio

    def a_diccionario(self):
        return {
            'tipo': self._tipo,
            'marca': self._marca,
            'modelo': self._modelo,
            'precio': self._precio,
            'fecha': self._fecha
        }