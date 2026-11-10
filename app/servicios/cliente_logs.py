import asyncio

async def registrar_evento_async(mensaje: str):
    """Envía un mensaje de log de manera asíncrona al servidor central."""
    host = '127.0.0.1'
    puerto = 9999
    try:
        reader, writer = await asyncio.open_connection(host, puerto)
        writer.write(mensaje.encode('utf-8'))
        await writer.drain()
        writer.close()
        await writer.wait_closed()
    except Exception:
        # Si el servidor de logs está apagado, la app no debe romperse por esto
        pass

# Función de ayuda síncrona por si la querés llamar desde código normal (no asíncrono)
def enviar_log(mensaje: str):
    try:
        asyncio.run(registrar_evento_async(mensaje))
    except RuntimeError:
        # Por si ya hay un loop de asyncio corriendo en el hilo actual
        loop = asyncio.get_event_loop()
        loop.run_until_complete(registrar_evento_async(mensaje))