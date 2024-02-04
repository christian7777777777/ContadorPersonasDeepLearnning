import tkinter as tk
from tkinter import ttk
import threading
import cv2
from ContadorPersonas import ContadorPersonas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PersonDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detección y conteo de personas")

        self.cap = cv2.VideoCapture(r"C:\Users\User\OneDrive\Escritorio\8tavo Semestre\Deep Learnning\Proyecto\ContadorPersonasDeepLearnning\Video\video.webm")

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        self.start_button = ttk.Button(self.main_frame, text="Iniciar", command=self.start_detection)
        self.start_button.pack(fill=tk.X, pady=10)

        self.stop_button = ttk.Button(self.main_frame, text="Detener", command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.pack(fill=tk.X, pady=10)

        self.zone_labels = []
        self.zone_labels_text = []
        for i in range(7):
            label_text = tk.StringVar() 
            label_text.set(f"Maximo de Detecciones en Zona {i+1}: 0 Personas")
            zone_label = ttk.Label(self.main_frame, textvariable=label_text)
            zone_label.pack()
            self.zone_labels.append(zone_label)
            self.zone_labels_text.append(label_text)

        self.show_graph_button = ttk.Button(self.main_frame, text="Mostrar Gráficas", command=self.show_graphs)
        self.show_graph_button.pack(fill=tk.X, pady=10)

        # Radiobuttons
        self.radio_var = tk.IntVar()
        for i in range(1, 5):
            ttk.Radiobutton(self.main_frame, text=f"Opción {i}", variable=self.radio_var, value=i).pack()

        # Gráficas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


    def start_detection(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        threading.Thread(target=self.detect_people).start()

    def stop_detection(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        self.cap.release()

    def detect_people(self):
        contador = ContadorPersonas()
        contador.detector(self.cap)
        self.maximos = contador.get_stadistics()

        for i, label in enumerate(self.zone_labels_text, start=0):
            label.set(f"Maximo de Detecciones en Zona {i+1}: {self.maximos[i]} Personas")

    def show_graphs(self):
        x = [1, 2, 3, 4, 5, 6, 7]
        y = self.maximos

        self.ax.set_title("Gráfica Aglomeración por Zonas")
        self.ax.stem(x, y)

        self.ax.set_xlabel("Zonas")
        self.ax.set_ylabel("Máximo de personas")

        self.canvas.draw()
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonDetectionApp(root)
    root.mainloop()
