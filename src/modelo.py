import numpy as np

def torricelli_edo(t, h, A_tanque, A_orificio, g=9.81):
    """
    Representa la EDO del vaciado de un tanque según la Ley de Torricelli.
    
    Parámetros:
    t: Tiempo (requerido por scipy.integrate)
    h: Altura actual del fluido en el tanque (metros)
    A_tanque: Área transversal del tanque (m^2)
    A_orificio: Área del orificio de salida (m^2)
    g: Aceleración de la gravedad (m/s^2)
    
    Retorna:
    dh/dt: La tasa de cambio de la altura respecto al tiempo.
    """
    # Condición de seguridad para evitar raíces negativas por imprecisiones numéricas
    if h <= 0:
        return 0.0
        
    return -(A_orificio / A_tanque) * np.sqrt(2 * g * h)

def calcular_area_circular(radio):
    """Calcula el área de un círculo dado su radio."""
    return np.pi * (radio ** 2)