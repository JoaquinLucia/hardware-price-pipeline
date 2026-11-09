class PrecioHistorico:
    def __init__(self, id_producto, monto, fecha=None, id_precio=None):
        self.id = id_precio
        self.id_producto = id_producto
        self.monto = monto
        self.fecha = fecha  # La base de datos la generará automáticamente si es None