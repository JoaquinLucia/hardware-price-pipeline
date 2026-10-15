from functools import wraps
from utilidades.cliente_socket import enviar_log_al_servidor

def decorador_log(funcion):
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        # Ejecutamos la función original
        resultado = funcion(*args, **kwargs)
        
        # Preparamos el mensaje de log
        mensaje = f"ACCION: {funcion.__name__} ejecutada. Resultado: {resultado}"
        
        # Aquí delegamos el envío del log al cliente socket (Punto 5)
        enviar_log_al_servidor(mensaje)
        
        return resultado
    return envoltura