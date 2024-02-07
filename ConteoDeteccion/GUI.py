import tkinter as tk                                                #Libreria para GUI
from tkinter import ttk                                             #Libreria para GUI
import threading                                                    #Libreria para ejecutar multiple Hilos en un mismo CPU
import cv2                                                          #Libreria para captura de Video
from ContadorPersonas import ContadorPersonas                       #Importacion de Metodo ContadorPersonas() de clase ContadorPersonas
import matplotlib.pyplot as plt                                     #Libreria para Graficas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg     #Libreria para Plot en GUI   

class PersonDetectionApp:

    def __init__(self, root):
        #Parametros de GUI
        self.root = root
        self.root.title("Detección y conteo de personas")

        #Lectura del video e instanciacion de la clase "ContadorPersonas()"
        self.cap = cv2.VideoCapture(r"C:\Users\User\OneDrive\Escritorio\8tavo Semestre\Deep Learnning\Proyecto\ContadorPersonasDeepLearnning\Video\video.webm")
        self.contador = ContadorPersonas()

        #Frame para el despliegue de Widgets de GUI
        self.main_frame = tk.Frame(self.root, border=5, borderwidth=5)
        self.main_frame.grid(row=0, column=0, columnspan=8, rowspan=13)

        #Metodo para crear los widgets en Framne de GUI
        self.create_widgets()

    def create_widgets(self):

        #Creacion de Botones para Iniciar y Detener proceso de "Deteccion y conteo de Personas"
        self.start_button = tk.Button(self.main_frame, text="Iniciar", command=self.start_detection, border=5, background="#B4C77F", foreground="black", borderwidth=5, font=("Times", 12), width=10)
        self.start_button.grid(row=0, column=0)
        self.stop_button = tk.Button(self.main_frame, text="Detener", command=self.stop_detection, state=tk.DISABLED, border=5, background="#FF8383", foreground="black", borderwidth=5, font=("Times", 12), width=10)
        self.stop_button.grid(row=0, column=1)

        #Varibles(listas) para almacenar widgets(Etiquetas y StringVar)
        self.zone_labels = []
        self.zone_labels_text = []

        #Ciclo para crear Labels de caza zona donde se mostraran metricas de conteo
        for i in range(7):
            label_text = tk.StringVar() 
            label_text.set(f"Personas en Zona {i+1}: 0 Personas")
            zone_label = ttk.Label(self.main_frame, textvariable=label_text)
            zone_label.grid(row=i+1, column=0, columnspan=2)
            self.zone_labels.append(zone_label)
            self.zone_labels_text.append(label_text)

        #Creacion de Boton para Graficar Datos de Aglomeracion global y por zonas
        self.show_graph_button = tk.Button(self.main_frame, text="Graficar", command=self.show_graphs, state=tk.DISABLED, border=5, background="#83C8FF", foreground="black", borderwidth=5, font=("Times", 12), width=5)
        self.show_graph_button.grid(row=9, column=1)

        #Creacion de ComboBox para desplegar opciones de Graficas
        valores = ["Aglomeracion Maxima Por zonas", 
            "Aglomercacion Zona 1",
            "Aglomercacion Zona 2",
            "Aglomercacion Zona 3",
            "Aglomercacion Zona 4",
            "Aglomercacion Zona 5",
            "Aglomercacion Zona 6",
            "Aglomercacion Zona 7"]
        self.Tipo_Grafica = ttk.Combobox(self.main_frame, values=valores, background="#AFC8DB", foreground="black", width=15, font=("Times", 12))
        self.Tipo_Grafica.current(0)
        self.Tipo_Grafica.grid(row=9, column=0)

        #Creacion de figura y Axis para el Graficado de los datos
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=9, column=2, rowspan=4, columnspan=6)

        #Creaion del Label para mostrar el video frame a frame dentro de GUI
        self.label_video = ttk.Label(self.main_frame, text="VIDEO")
        self.label_video.grid(row=0, column=2, rowspan=8, columnspan=6)

    #Metodo de Inicio de Proceso(Deteccion y conteo de Personas)
    def start_detection(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        #Creacion de Hilo para optimizar el proceso
        threading.Thread(target=self.detect_people).start()

    #Metodo para detener el proceso de deteccion
    def stop_detection(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.show_graph_button.config(state=tk.NORMAL)

        self.cap.release()

    #Metodo para utilizar la funcion (detector() de la clase Instanciada)
    def detect_people(self):

        #Pasamos los parametros que necesita el metodo detector como:
        #   cap -> VideoCapure()
        #   Label_video -> Label donde se mostrara el video
        #   zona_label_text -> StringVar para ser modificadas con metricas de conteo
        self.contador.detector(self.cap, self.label_video, self.zone_labels_text)
        
        #Obtencion de Cantidad Maxima de Personas detectadas en cada Zona
        self.maximos = self.contador.get_stadistics()

    #Metodo para graficar Datos obtenidos
    def show_graphs(self):

        #Limpiar Axis de la grafica anterior
        self.ax.clear()

        #Obtencion de Seleccion de Tipo de Grafica del ComboBox
        tipoGrafica = self.Tipo_Grafica.get()

        #Condicional para Dibujar en el Axis el tipo de grafica seleccionado
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
        
        #Despliege de la grafica
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonDetectionApp(root)
    root.mainloop()
