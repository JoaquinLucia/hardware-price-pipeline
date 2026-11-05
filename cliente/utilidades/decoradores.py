from functools import wraps
from .cliente_socket import enviar_log_al_servidor

def decorador_log(funcion):
    """
    Decorador que intercepta la ejecución de funciones,
    genera un log de auditoría y lo envía por Socket.
    """
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        resultado = funcion(*args, **kwargs)
        mensaje_log = f"DECORADOR: Accion '{funcion.__name__}' ejecutada | Resultado: {resultado}"
        enviar_log_al_servidor(mensaje_log)
        return resultado
    return envoltura