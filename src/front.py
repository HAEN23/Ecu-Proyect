import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InterfazSimulador:
    """
    Interfaz gráfica principal para el Simulador de Vaciado de Tanque.
    Permite ingresar los parámetros físicos del sistema y lanzar la simulación.
    """

    def __init__(self, raiz, callback_simular):
        self.raiz = raiz
        self.raiz.title("Simulador de Vaciado de Tanque - Ley de Torricelli")
        self.raiz.geometry("680x760")
        self.raiz.resizable(False, False)
        self.raiz.configure(bg="#f0f4f8")

        self._construir_interfaz(callback_simular)
        self._crear_seccion_grafica()

    # ─────────────────────────────────────────────
    # CONSTRUCCIÓN DE LA INTERFAZ
    # ─────────────────────────────────────────────

    def _construir_interfaz(self, callback_simular):
        """Construye todos los widgets de la ventana."""
        self._crear_encabezado()
        self._crear_seccion_tanque()
        self._crear_seccion_orificio()
        self._crear_seccion_escenario()
        self._crear_boton_simular(callback_simular)
        self._crear_barra_estado()

    def _crear_encabezado(self):
        """Título y subtítulo del simulador."""
        marco = tk.Frame(self.raiz, bg="#2c3e50", pady=12)
        marco.pack(fill="x")

        tk.Label(
            marco, text="Simulador de Vaciado de Tanque",
            font=("Arial", 14, "bold"), bg="#2c3e50", fg="white"
        ).pack()

        tk.Label(
            marco, text="Modelo basado en la Ley de Torricelli    dh/dt = -k√h",
            font=("Arial", 9), bg="#2c3e50", fg="#aab7c4"
        ).pack()

    def _crear_seccion_tanque(self):
        """Campos para los parámetros físicos del tanque."""
        marco = self._crear_marco_seccion(" Parámetros del Tanque")

        self.entrada_radio_tanque = self._crear_campo(
            marco, "Radio del tanque (m):", "0.55", fila=0,
            ayuda="Radio interno del tinaco en metros"
        )
        self.entrada_altura_inicial = self._crear_campo(
            marco, "Altura inicial del agua (m):", "1.17", fila=1,
            ayuda="Nivel del agua al inicio de la simulación" 
        
        )
      

    def _crear_seccion_orificio(self):
        """Campos para los parámetros del orificio de salida."""
        marco = self._crear_marco_seccion("🔩 Parámetros del Orificio")

        self.entrada_radio_orificio = self._crear_campo(
            marco, "Radio del orificio (m):", "0.019", fila=0,
            ayuda="Radio del orificio de salida en metros"
        )   
        self.entrada_coef_descarga = self._crear_campo(
            marco, "Coeficiente de descarga (Cd):", "0.6", fila=1,
            ayuda="Factor de corrección del flujo (0 a 1)"
        )

    def _crear_seccion_escenario(self):
        marco = self._crear_marco_seccion("Escenario de Simulación")

        self.variable_escenario = tk.IntVar(value=1)

        escenarios = [
            (1, "Fuga grande  (r = 0.019 m)"),
            (2, "Consumo normal  (r = 0.00635 m)"),
            (3, "Fuga pequeña (r = 0.003 m)"),
            (4, "Personalizado ")
        ]

        for valor, texto in escenarios:
            tk.Radiobutton(
                marco, text=texto, variable=self.variable_escenario, value=valor,
                bg="#ffffff", anchor="w", font=("Arial", 9),
                command=self._aplicar_escenario
            ).pack(fill="x", padx=10, pady=2)

    def _crear_boton_simular(self, callback_simular):
        """Botón principal para ejecutar la simulación."""
        tk.Button(
            self.raiz, text="▶  EJECUTAR SIMULACIÓN",
            bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
            activebackground="#1e8449", cursor="hand2",
            command=callback_simular, pady=8
        ).pack(fill="x", padx=20, pady=(10, 5))

    def _crear_barra_estado(self):
        """Etiqueta de estado en la parte inferior."""
        self.etiqueta_estado = tk.Label(
            self.raiz, text="Listo para iniciar.",
            font=("Arial", 9), bg="#f0f4f8", fg="gray"
        )
        self.etiqueta_estado.pack(side="bottom", pady=8)

    def _crear_seccion_grafica(self):
        """Canvas embebido donde se mostrará la gráfica tras la simulación."""
        marco = self._crear_marco_seccion("📈 Resultado: Altura vs Tiempo")

        figura = Figure(figsize=(5, 2.8), dpi=90)
        self.eje = figura.add_subplot(111)
        self.eje.set_xlabel("Tiempo (s)")
        self.eje.set_ylabel("Altura (m)")
        self.eje.set_title("Ejecuta la simulación para ver la gráfica")
        self.eje.grid(True, linestyle="--", alpha=0.6)

        self.canvas_grafica = FigureCanvasTkAgg(figura, master=marco)
        self.canvas_grafica.get_tk_widget().pack(fill="both", expand=True)


    def _crear_marco_seccion(self, titulo):
        """Crea un marco con borde y título para agrupar campos."""
        contenedor = tk.LabelFrame(
            self.raiz, text=titulo, font=("Arial", 10, "bold"),
            bg="#ffffff", fg="#2c3e50", padx=10, pady=8, relief="groove"
        )
        contenedor.pack(fill="x", padx=15, pady=6)
        return contenedor

    def _crear_campo(self, padre, etiqueta, valor_defecto, fila, ayuda=""):
        """Crea una fila con etiqueta, campo de entrada y texto de ayuda."""
        tk.Label(
            padre, text=etiqueta, bg="#ffffff",
            font=("Arial", 9), anchor="w", width=28
        ).grid(row=fila, column=0, sticky="w", pady=3)

        entrada = tk.Entry(padre, width=12, font=("Arial", 10))
        entrada.insert(0, valor_defecto)
        entrada.grid(row=fila, column=1, padx=5)

        if ayuda:
            tk.Label(
                padre, text=f"ℹ {ayuda}", bg="#ffffff",
                font=("Arial", 7), fg="#7f8c8d"
            ).grid(row=fila, column=2, padx=4, sticky="w")

        return entrada

    # ─────────────────────────────────────────────
    # LÓGICA DE ESCENARIOS
    # ─────────────────────────────────────────────

    def _aplicar_escenario(self):
        """Actualiza el radio del orificio según el escenario seleccionado."""
        escenario = self.variable_escenario.get()
        if escenario == 1:
            self._establecer_valor(self.entrada_radio_orificio, "0.019")
        elif escenario == 2:
            self._establecer_valor(self.entrada_radio_orificio, "0.00635")
        elif escenario == 3:
            self._establecer_valor(self.entrada_radio_orificio, "0.003")
        # Escenario 4: personalizado, el usuario ingresa manualmente

    def _establecer_valor(self, entrada, valor):
        """Reemplaza el contenido de un campo de entrada."""
        entrada.delete(0, tk.END)
        entrada.insert(0, valor)

    # ─────────────────────────────────────────────
    # MÉTODOS PÚBLICOS
    # ─────────────────────────────────────────────

    def obtener_parametros(self):
        """
        Retorna un diccionario con todos los parámetros ingresados por el usuario.
        Lanza ValueError si algún campo tiene un valor inválido.
        """
        try:
            parametros = {
                "radio_tanque":   float(self.entrada_radio_tanque.get()),
                "altura_inicial": float(self.entrada_altura_inicial.get()),
                "radio_orificio": float(self.entrada_radio_orificio.get()),
                "coef_descarga":  float(self.entrada_coef_descarga.get()),
                "escenario":      self.variable_escenario.get(),
            }
        except ValueError:
            raise ValueError("Todos los campos deben contener valores numéricos válidos.")

        # Validaciones básicas
        if parametros["radio_tanque"] <= 0:
            raise ValueError("El radio del tanque debe ser mayor a 0.")
        if not (0 < parametros["altura_inicial"] <= 10):
            raise ValueError("La altura inicial debe estar entre 0 y 10 metros.")
        if not (0 < parametros["coef_descarga"] <= 1):
            raise ValueError("El coeficiente de descarga debe estar entre 0 y 1.")

        return parametros

    def actualizar_estado(self, mensaje, color="black"):
        """Actualiza el texto de la barra de estado."""
        self.etiqueta_estado.config(text=mensaje, fg=color)

    def mostrar_grafica(self, tiempos, alturas):
        """Dibuja la curva de altura vs tiempo en el canvas embebido."""
        self.eje.clear()
        self.eje.plot(tiempos, alturas, color="#1f77b4", linewidth=2, label="Nivel del fluido")
        self.eje.set_xlabel("Tiempo (s)")
        self.eje.set_ylabel("Altura (m)")
        self.eje.set_title("Proceso de Vaciado del Tanque")
        self.eje.legend()
        self.eje.grid(True, linestyle="--", alpha=0.6)
        self.canvas_grafica.draw()


# ─────────────────────────────────────────────
# PRUEBA RÁPIDA (ejecutar directamente este archivo)
# ─────────────────────────────────────────────
if __name__ == "__main__":
    def simular():
        try:
            datos = app.obtener_parametros()
            app.actualizar_estado(f"Parámetros OK — Altura: {datos['altura_inicial']} m", "green")
            print("Parámetros recibidos:", datos)
        except ValueError as error:
            app.actualizar_estado(str(error), "red")

    raiz = tk.Tk()
    app = InterfazSimulador(raiz, simular)
    raiz.mainloop()
