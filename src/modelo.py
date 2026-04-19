import numpy as np

def torricelli_edo(t, h, area_tanque, area_orificio, gravedad=9.81, coef_descarga=1.0):
    """
    EDO del vaciado de un tanque según la Ley de Torricelli.

    Parámetros:
        t            : Tiempo actual (requerido por scipy)
        h            : Altura actual del fluido (metros)
        area_tanque  : Área transversal del tanque (m²)
        area_orificio: Área del orificio de salida (m²)
        gravedad     : Aceleración gravitacional (m/s²)
        coef_descarga: Factor de corrección del flujo, Cd (0 a 1)

    Retorna:
        dh/dt: Tasa de cambio de la altura respecto al tiempo
    """
    if h <= 0:
        return 0.0

    return -(coef_descarga * area_orificio / area_tanque) * np.sqrt(2 * gravedad * h)

def calcular_area_circular(radio):
    """Calcula el área de un círculo dado su radio en metros."""
    return np.pi * (radio ** 2)
