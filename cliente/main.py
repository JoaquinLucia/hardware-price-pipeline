import tkinter as tk
from modelo.gestor_precios import GestorPrecios
from modelo.observador_socket import ObservadorSocket
from controlador.controlador import Controlador
from vista.gui import VistaPrincipal

def main():
    # 1. Instanciamos el Modelo de Negocio (Sujeto)
    gestor_precios = GestorPrecios()

    # 2. Instanciamos el Observador de Sockets y lo suscribimos al Modelo
    # Cada vez que haya un éxito/error en la BD, mandará un log por red
    observador_red = ObservadorSocket()
    gestor_precios.agregar_observador(observador_red)

    # 3. Instanciamos el Controlador, inyectándole el modelo
    controlador = Controlador(gestor_precios)

    # 4. Inicializamos Tkinter y la Vista
    root = tk.Tk()
    vista = VistaPrincipal(root, controlador)
    controlador.set_vista(vista)

    # 5. Suscribimos la Vista al Modelo
    # Así la tabla se actualiza sola sin que el controlador le tenga que decir
    gestor_precios.agregar_observador(vista)

    # 6. Arrancamos el loop de la interfaz
    root.mainloop()

if __name__ == "__main__":
    main()