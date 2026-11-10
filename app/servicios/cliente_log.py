import asyncio

class ClienteSocketLog:
    def __init__(self, host='127.0.0.1', puerto=9999):
        self.host = host
        self.puerto = puerto

    async def enviar_mensaje_async(self, mensaje: str):
        """Abre una conexión TCP asíncrona, transmite el log y cierra el socket."""
        try:
            reader, writer = await asyncio.open_connection(self.host, self.puerto)
            writer.write(mensaje.encode('utf-8'))
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        except ConnectionRefusedError:
            pass
        except Exception as e:
            print(f"[ERROR SOCKET ASYNC] {e}")

    def enviar_mensaje(self, mensaje: str):
        """Permite llamar al cliente asíncrono desde funciones normales (síncronas)."""
        try:
            asyncio.run(self.enviar_mensaje_async(mensaje))
        except RuntimeError:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.enviar_mensaje_async(mensaje))
            else:
                loop.run_until_complete(self.enviar_mensaje_async(mensaje))

# Instancia global requerida por observador.py
cliente_log_global = ClienteSocketLog()

# Función helper para llamadas directas
def enviar_log(mensaje: str):
    cliente_log_global.enviar_mensaje(mensaje)