import tkinter as tk
from tkinter import ttk

class InterfazTanque:
    def __init__(self, root, callback_simular):
        self.root = root
        self.root.title("Simulador de Vaciado - Frontend")
        self.root.geometry("400x450")
        
        # Títulos
        tk.Label(root, text="Configuración Visual", font=("Arial", 14, "bold")).pack(pady=10)

        # Campos de entrada
        self.entry_radio = self._crear_campo("Radio del Tanque (m):", "0.55")
        self.entry_altura = self._crear_campo("Altura Inicial (m):", "1.17")

        # Selector de Escenario
        tk.Label(root, text="Tamaño del Orificio:", font=("Arial", 10, "bold")).pack(pady=5)
        self.var_escenario = tk.IntVar(value=1)
        tk.Radiobutton(root, text="Tubo 1.5\" (Fuga)", variable=self.var_escenario, value=1).pack()
        tk.Radiobutton(root, text="Llave 1/2\" (Consumo)", variable=self.var_escenario, value=2).pack()

        # Botón que llama a la lógica externa
        self.btn_simular = tk.Button(
            root, text="EJECUTAR SIMULACIÓN", 
            bg="#2c3e50", fg="white", font=("Arial", 10, "bold"),
            command=callback_simular
        )
        self.btn_simular.pack(pady=20, ipadx=10, ipady=5)

        # Barra de estado
        self.lbl_estado = tk.Label(root, text="Listo para iniciar", fg="gray")
        self.lbl_estado.pack(side="bottom", pady=10)

    def _crear_campo(self, texto, valor_defecto):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Label(frame, text=texto, width=20, anchor="e").grid(row=0, column=0, padx=5)
        entry = tk.Entry(frame, width=10)
        entry.insert(0, valor_defecto)
        entry.grid(row=0, column=1)
        return entry

    def obtener_datos(self):
        return {
            "radio": float(self.entry_radio.get()),
            "altura": float(self.entry_altura.get()),
            "escenario": self.var_escenario.get()
        }

    def actualizar_estado(self, mensaje, color="black"):
        self.lbl_estado.config(text=mensaje, fg=color)