import tkinter as tk
from tkinter import ttk, messagebox
from modelo.observador import Observador

class VistaPrincipal(Observador):
    def __init__(self, root, controlador):
        self.root = root
        self.root.title("Pipeline de Precios de Hardware")
        self.root.geometry("600x450")
        self.controlador = controlador
        
        self._construir_interfaz()
        self._cargar_tabla()

    def _construir_interfaz(self):
        # Frame de Entrada
        frame_inputs = tk.LabelFrame(self.root, text="Simular Ingesta de Precio")
        frame_inputs.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_inputs, text="Tipo:").grid(row=0, column=0, padx=5, pady=5)
        self.var_tipo = tk.StringVar()
        ttk.Combobox(frame_inputs, textvariable=self.var_tipo, values=["Procesador", "Motherboard", "Placa de Video", "Monitor"]).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_inputs, text="Marca:").grid(row=0, column=2, padx=5, pady=5)
        self.var_marca = tk.StringVar()
        tk.Entry(frame_inputs, textvariable=self.var_marca).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_inputs, text="Modelo:").grid(row=1, column=0, padx=5, pady=5)
        self.var_modelo = tk.StringVar()
        tk.Entry(frame_inputs, textvariable=self.var_modelo).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_inputs, text="Precio ($):").grid(row=1, column=2, padx=5, pady=5)
        self.var_precio = tk.StringVar()
        tk.Entry(frame_inputs, textvariable=self.var_precio).grid(row=1, column=3, padx=5, pady=5)

        tk.Button(frame_inputs, text="Registrar", command=self._boton_registrar, bg="lightblue").grid(row=2, column=0, columnspan=4, pady=10)

        # Frame Tabla
        self.tree = ttk.Treeview(self.root, columns=("ID", "Tipo", "Marca", "Modelo", "Precio", "Fecha"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def _boton_registrar(self):
        resultado = self.controlador.registrar_ingesta(
            self.var_tipo.get(), self.var_marca.get(), self.var_modelo.get(), self.var_precio.get()
        )
        if resultado != "OK":
            messagebox.showerror("Error de Ingreso", resultado)

    def _cargar_tabla(self):
        # Limpiamos la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Cargamos los datos del controlador
        for fila in self.controlador.obtener_datos():
            self.tree.insert("", "end", values=fila)

    def actualizar(self, evento, detalle):
        """
        ¡MAGIA DEL OBSERVER!
        Cuando el Gestor de BD inserta un registro, avisa a la Vista.
        """
        if evento == "NUEVO_REGISTRO":
            self._cargar_tabla()
            print(f"[VISTA] Tabla actualizada por evento. Detalle: {detalle}")
        elif evento == "ERROR_BD":
            messagebox.showerror("Error en Base de Datos", detalle)