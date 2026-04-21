# Simulador de Vaciado de Tanque - Ley de Torricelli 💧

Proyecto aplicado para el modelado, simulación y análisis del proceso de vaciado de un tanque (tinaco doméstico) utilizando Ecuaciones Diferenciales Ordinarias (EDO). Desarrollado como parte de los proyectos de Ingeniería en Tecnología de Software de la Universidad Politécnica de Chiapas.

## Descripción del Proyecto
Este simulador resuelve numéricamente la ecuación diferencial basada en la **Ley de Torricelli** para predecir el tiempo de vaciado de un tanque bajo distintos escenarios (fugas de emergencia vs. consumo diario). Cuenta con una Interfaz Gráfica de Usuario (GUI) que permite interactuar con los parámetros físicos y exporta automáticamente los resultados visuales.

### Características Principales
- **Cálculo Numérico:** Resolución de la EDO paso a paso utilizando el método Runge-Kutta 4(5) a través de `scipy.integrate`.
- **Interfaz Interactiva:** Frontend construido con `tkinter` para ingresar el radio del tanque, altura inicial y escenarios de consumo de forma dinámica.
- **Exportación Visual:** Generación automática de gráficas estáticas (Altura vs Tiempo) y simulaciones animadas en formato `.gif`.
- **Arquitectura Separada:** División clara entre la lógica matemática (Backend) y el diseño de la ventana (Frontend).

## Tecnologías y Librerías Utilizadas
El proyecto está desarrollado en **Python 3** y hace uso de las siguientes librerías científicas y visuales:
- `numpy`: Cálculos matemáticos y manejo de arreglos.
- `scipy`: Motor de integración numérica (`solve_ivp`).
- `matplotlib` y `pillow`: Trazado de gráficas y renderizado de la animación GIF.
- `tkinter`: Construcción de la interfaz gráfica nativa.



