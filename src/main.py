import tkinter as tk
from tkinter import messagebox
from scipy.integrate import solve_ivp

from front import InterfazSimulador
from modelo import torricelli_edo, calcular_area_circular
from animacion import generar_gif

def controlador_simulacion():
    try:
        # 1. Obtener parámetros desde la interfaz
        parametros = app.obtener_parametros()

        # 2. Calcular áreas
        area_tanque   = calcular_area_circular(parametros["radio_tanque"])
        area_orificio = calcular_area_circular(parametros["radio_orificio"])

        app.actualizar_estado("Calculando física...", "blue")

        # 3. Resolver la EDO con la Ley de Torricelli
        solucion = solve_ivp(
            fun=lambda t, y: torricelli_edo(
                t, y[0], area_tanque, area_orificio,
                coef_descarga=parametros["coef_descarga"]
            ),
            t_span=(0, 86400),
            y0=[parametros["altura_inicial"]],
            events=lambda t, y: y[0] - 0.001,  # detener cuando h ≈ 0
            max_step=1.0
        )

        # 4. Mostrar gráfica en la interfaz y generar GIF
        app.actualizar_estado("Generando archivos visuales...", "orange")
        app.mostrar_grafica(solucion.t, solucion.y[0])
        generar_gif(solucion.t, solucion.y[0], parametros["radio_tanque"], parametros["altura_inicial"])

        app.actualizar_estado("¡Éxito! Revisa la carpeta output/", "green")
        messagebox.showinfo("Simulación completada", "Los archivos fueron guardados en output/")

    except ValueError as error:
        app.actualizar_estado(str(error), "red")
        messagebox.showerror("Datos inválidos", str(error))
    except Exception as error:
        app.actualizar_estado("Error inesperado", "red")
        messagebox.showerror("Error", str(error))

# ─────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────
if __name__ == "__main__":
    raiz = tk.Tk()
    
    # --- CAMBIO AGREGADO AQUÍ ---
    # Permite que la ventana se pueda maximizar y estirar libremente
    raiz.resizable(True, True) 
    # ----------------------------

    app = InterfazSimulador(raiz, controlador_simulacion)
    raiz.mainloop()