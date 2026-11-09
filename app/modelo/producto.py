class Producto:
    def __init__(self, nombre, url, tienda, categoria="General", id_producto=None):
        self.id = id_producto
        self.nombre = nombre
        self.url = url
        self.tienda = tienda
        self.categoria = categoria