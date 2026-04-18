import tkinter as tk
from tkinter import messagebox
from scipy.integrate import solve_ivp

# Importamos las piezas del rompecabezas
from gui import InterfazTanque
from modelo import torricelli_edo, calcular_area_circular
from animacion import generar_grafica, generar_gif

def controlador_simulacion():
    try:
        # 1. Obtenemos datos del "Frontend"
        datos = app.obtener_datos()
        
        # 2. Lógica de negocio (Backend)
        radio_o = 0.019 if datos["escenario"] == 1 else 0.00635
        A_t = calcular_area_circular(datos["radio"])
        A_o = calcular_area_circular(radio_o)
        
        app.actualizar_estado("Calculando física...", "blue")
        
        # Resolución de la EDO [cite: 13, 23]
        sol = solve_ivp(
            fun=lambda t, y: torricelli_edo(t, y[0], A_t, A_o),
            t_span=(0, 86400), y0=[datos["altura"]],
            events=lambda t, y: y[0] - 0.001
        )
        sol.y_events[0] = True # Para detener el proceso
        
        # 3. Generación de archivos de salida [cite: 58, 59]
        app.actualizar_estado("Generando archivos visuales...", "orange")
        generar_grafica(sol.t, sol.y[0])
        generar_gif(sol.t, sol.y[0], datos["radio"], datos["altura"])
        
        app.actualizar_estado("¡Éxito! Revisa la carpeta output/", "green")
        messagebox.showinfo("Completado", "Simulación terminada.")

    except Exception as e:
        app.actualizar_estado("Error en el proceso", "red")
        messagebox.showerror("Error", str(e))

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazTanque(root, controlador_simulacion)
    root.mainloop()