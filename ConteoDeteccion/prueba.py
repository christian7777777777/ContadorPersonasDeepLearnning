from tkinter import ttk
import tkinter as tk
root = tk.Tk()
frame = ttk.Frame(root)
frame.pack()

# Creamos un estilo personalizado
style = ttk.Style()
style.configure(
    "MyButton.TButton",
    foreground="#ff0000",
    background="#FF8383",
    padding=10,
    font=("Times", 12),
    anchor="w"
)
# Creamos dos botones
button1 = ttk.Button(frame, text="Botón 1", style="MyButton.TButton")
button2 = tk.Button(frame, text="Botón 2", border=5, background="#B4C77F", foreground="black", borderwidth=5, font=("Times", 12), width=10)

# Aplicamos el estilo a los botones

# Colocamos los botones en la ventana
button1.pack()
button2.pack()

root.mainloop()