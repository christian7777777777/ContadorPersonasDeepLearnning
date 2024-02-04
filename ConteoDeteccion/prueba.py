import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def graficar():
    # Borrar gráfico anterior
    ax.clear()

    # Obtener la función seleccionada
    funcion = combo_funciones.get()

    # Definir los valores de x
    x = np.linspace(-2*np.pi, 2*np.pi, 100)

    # Calcular la función correspondiente
    if funcion == "seno":
        y = np.sin(x)
    elif funcion == "coseno":
        y = np.cos(x)
    elif funcion == "tangente":
        y = np.tan(x)

    # Graficar la función
    ax.plot(x, y)
    ax.set_title(funcion.capitalize())
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    canvas.draw()


# Crear la ventana principal
root = tk.Tk()
root.title("Gráfico de funciones")

# Crear el lienzo para el gráfico
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Crear el combo box para seleccionar la función
funciones = ["seno", "coseno", "tangente"]
combo_funciones = ttk.Combobox(root, values=funciones)
combo_funciones.current(0)
combo_funciones.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, pady=10)

# Crear el botón para graficar
boton_graficar = tk.Button(root, text="Graficar", command=graficar)
boton_graficar.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1, pady=10)

# Ejecutar la aplicación
root.mainloop()