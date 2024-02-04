import tkinter as tk
from tkinter import ttk
import threading
import cv2
from ContadorPersonas import ContadorPersonas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.cm as cm
import numpy as np

class PersonDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detección y conteo de personas")

        self.cap = cv2.VideoCapture(r"C:\Users\User\OneDrive\Escritorio\8tavo Semestre\Deep Learnning\Proyecto\ContadorPersonasDeepLearnning\Video\video.webm")
        self.contador = ContadorPersonas()

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

        valores = ["Aglomeracion Maxima Por zonas", 
            "Aglomercacion Zona 1",
            "Aglomercacion Zona 2",
            "Aglomercacion Zona 3",
            "Aglomercacion Zona 4",
            "Aglomercacion Zona 5",
            "Aglomercacion Zona 6",
            "Aglomercacion Zona 7"]
        
        self.Tipo_Grafica = ttk.Combobox(self.main_frame, values=valores)
        self.Tipo_Grafica.current(0)
        self.Tipo_Grafica.pack(pady=10)
        
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
        self.contador.detector(self.cap)
        self.maximos = self.contador.get_stadistics()

        for i, label in enumerate(self.zone_labels_text, start=0):
            label.set(f"Maximo de Detecciones en Zona {i+1}: {self.maximos[i]} Personas")

    def show_graphs(self):
        self.ax.clear()

        tipoGrafica = self.Tipo_Grafica.get()

        if tipoGrafica == "Aglomeracion Maxima Por zonas":
            x = ["Zona 1", "Zona 2", "Zona 3", "Zona 4", "Zona 5", "Zona 6", "Zona 7"]
            y = self.maximos
            self.ax.set_title("Gráfica Aglomeración por Zonas")
            self.ax.bar(x, y, color="skyblue")
            self.ax.grid(True)
            self.ax.set_xlabel("Zonas")
            self.ax.set_ylabel("Máximo de personas")

        elif tipoGrafica == "Aglomercacion Zona 1":
            x, y = self.contador.get_stadistics_zone(0)
            self.ax.set_title("Gráfica Aglomeración Zona 1")
            self.ax.plot(x, y, color='green', label='Zona 1')
            self.ax.grid(True)
            self.ax.set_xlabel("Frame")
            self.ax.set_ylabel("Personas por Frame")
        elif tipoGrafica == "Aglomercacion Zona 2":
            x, y = self.contador.get_stadistics_zone(1)
            self.ax.set_title("Gráfica Aglomeración Zona 2")
            self.ax.plot(x, y, color='green', label='Zona 2')
            self.ax.grid(True)
            self.ax.set_xlabel("Frame")
            self.ax.set_ylabel("Personas por Frame")
        elif tipoGrafica == "Aglomercacion Zona 3":
            x, y = self.contador.get_stadistics_zone(2)
            self.ax.set_title("Gráfica Aglomeración Zona 3")
            self.ax.plot(x, y, color='green', label='Zona 3')
            self.ax.grid(True)
            self.ax.set_xlabel("Frame")
            self.ax.set_ylabel("Personas por Frame")
        elif tipoGrafica == "Aglomercacion Zona 4":
            x, y = self.contador.get_stadistics_zone(3)
            self.ax.set_title("Gráfica Aglomeración Zona 4")
            self.ax.plot(x, y, color='green', label='Zona 4')
            self.ax.grid(True)
            self.ax.set_xlabel("Frame")
            self.ax.set_ylabel("Personas por Frame")
        elif tipoGrafica == "Aglomercacion Zona 5":
            x, y = self.contador.get_stadistics_zone(4)
            self.ax.set_title("Gráfica Aglomeración Zona 5")
            self.ax.plot(x, y, color='green', label='Zona 5')
            self.ax.grid(True)
            self.ax.set_xlabel("Frame")
            self.ax.set_ylabel("Personas por Frame")
        elif tipoGrafica == "Aglomercacion Zona 6":
            x, y = self.contador.get_stadistics_zone(5)
            self.ax.set_title("Gráfica Aglomeración Zona 6")
            self.ax.plot(x, y, color='green', label='Zona 6')
            self.ax.grid(True)
            self.ax.set_xlabel("Frame")
            self.ax.set_ylabel("Personas por Frame")
        elif tipoGrafica == "Aglomercacion Zona 7":
            x, y = self.contador.get_stadistics_zone(6)
            self.ax.set_title("Gráfica Aglomeración Zona 7")
            self.ax.plot(x, y, color='green', label='Zona 7')
            self.ax.grid(True)
            self.ax.set_xlabel("Frame")
            self.ax.set_ylabel("Personas por Frame")
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonDetectionApp(root)
    root.mainloop()
