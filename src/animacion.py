import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

def asegurar_directorio(ruta):
    """Crea el directorio de salida si no existe."""
    directorio = os.path.dirname(ruta)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)

def generar_grafica(tiempos, alturas, ruta_salida="output/altura_vs_tiempo.png"):
    """
    Genera y guarda una gráfica de línea del nivel del agua a lo largo del tiempo.
    """
    print("Generando gráfica de Altura vs Tiempo...")
    asegurar_directorio(ruta_salida)
    
    plt.figure(figsize=(8, 5))
    plt.plot(tiempos, alturas, color="#1f77b4", linewidth=2, label="Nivel del fluido")
    
    plt.title("Proceso de Vaciado del Tanque")
    plt.xlabel("Tiempo (segundos)")
    plt.ylabel("Altura (metros)")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(ruta_salida, dpi=300)
    plt.close()
    print(f"-> Gráfica guardada exitosamente en: {ruta_salida}")

def generar_gif(tiempos, alturas, radio_tanque, altura_maxima, ruta_salida="output/simulacion.gif"):
    """
    Crea una animación visual del tanque vaciándose y la exporta como GIF.
    """
    print("Generando animación GIF (esto puede tomar unos segundos)...")
    asegurar_directorio(ruta_salida)
    
    fig, ax = plt.subplots(figsize=(4, 6))
    
    # Para evitar que el GIF sea demasiado pesado, seleccionamos un máximo de ~100 frames
    total_puntos = len(tiempos)
    salto = max(1, total_puntos // 100)
    t_frames = tiempos[::salto]
    h_frames = alturas[::salto]
    
    # Configurar los límites visuales de la gráfica
    ax.set_xlim(-radio_tanque * 1.5, radio_tanque * 1.5)
    ax.set_ylim(-0.1, altura_maxima * 1.2)
    ax.set_aspect('equal')
    ax.axis('off') # Ocultar los ejes numéricos para una apariencia más limpia
    
    # Dibujar el contorno del tanque (rectángulo vacío)
    tanque_outline = patches.Rectangle(
        (-radio_tanque, 0), radio_tanque * 2, altura_maxima, 
        fill=False, edgecolor='black', linewidth=3
    )
    ax.add_patch(tanque_outline)
    
    # Dibujar el fluido inicial (rectángulo relleno)
    fluido = patches.Rectangle(
        (-radio_tanque, 0), radio_tanque * 2, h_frames[0], 
        fill=True, color='#87CEEB' # Color azul cielo
    )
    ax.add_patch(fluido)
    
    # Texto dinámico en la parte superior para mostrar el tiempo y altura
    texto_info = ax.text(0, altura_maxima * 1.05, '', ha='center', fontsize=11, fontweight='bold')
    
    def actualizar(frame):
        """Función que actualiza cada frame de la animación."""
        h_actual = h_frames[frame]
        t_actual = t_frames[frame]
        
        # Actualizar la altura del rectángulo del fluido
        fluido.set_height(h_actual)
        # Actualizar el texto
        texto_info.set_text(f"Tiempo: {t_actual:.1f} s | Altura: {h_actual:.3f} m")
        
        return fluido, texto_info
    
    # Crear la animación
    ani = animation.FuncAnimation(
        fig, actualizar, frames=len(h_frames), 
        interval=50, blit=True
    )
    
    # Guardar la animación (Requiere la librería 'Pillow' o 'ImageMagick')
    ani.save(ruta_salida, writer='pillow', fps=20)
    plt.close()
    print(f"-> Animación guardada exitosamente en: {ruta_salida}")