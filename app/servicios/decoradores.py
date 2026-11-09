import functools
import time
from app.servicios.observador import gestor_logs_global

def registro_log_scraper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        gestor_logs_global.notificar("INFO", f"Iniciando ejecución de '{func.__name__}'...")
        
        try:
            resultado = func(*args, **kwargs)
            fin = time.time()
            
            tiempo_total = fin - inicio
            gestor_logs_global.notificar("EXITO", f"'{func.__name__}' finalizó correctamente en {tiempo_total:.2f} segundos.")
            
            return resultado
        
        except Exception as e:
            gestor_logs_global.notificar("ERROR", f"Fallo en '{func.__name__}': {str(e)}")
            raise e 
            
    return wrapper