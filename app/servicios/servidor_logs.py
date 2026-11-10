import asyncio
import os
from datetime import datetime

DIRECTORIO_LOGS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
ARCHIVO_LOG = os.path.join(DIRECTORIO_LOGS, 'sistema_hardware.log')

HOST = '127.0.0.1'
PUERTO = 9999

async def manejar_cliente(reader, writer):
    data = await reader.read(1024)
    mensaje = data.decode('utf-8')
    direccion = writer.get_extra_info('peername')
    
    if mensaje:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        registro = f"[{timestamp}] - CLIENTE ({direccion[0]}): {mensaje.strip()}\n"
        
        os.makedirs(DIRECTORIO_LOGS, exist_ok=True)
        with open(ARCHIVO_LOG, 'a', encoding='utf-8') as f:
            f.write(registro)
            
        print(f"[LOG RECIBIDO ASÍNCRONO] {mensaje.strip()}")
        
    writer.close()
    await writer.wait_closed()

async def main():
    servidor = await asyncio.start_server(manejar_cliente, HOST, PUERTO)
    addr = servidor.sockets[0].getsockname()
    print(f"[*] Servidor de Logs Asíncrono escuchando en {addr}...")

    async with servidor:
        await servidor.serve_forever()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Servidor detenido correctamente.")