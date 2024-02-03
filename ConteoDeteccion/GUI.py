import tkinter as tk
from tkinter import ttk
import threading
import cv2
from ContadorPersonas import detector

class PersonDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detección y conteo de personas")

        self.cap = cv2.VideoCapture(r"C:\Users\User\OneDrive\Escritorio\8tavo Semestre\Deep Learnning\Proyecto\ContadorPersonasDeepLearnning\Video\video.webm")

        self.create_widgets()

    def create_widgets(self):
        self.start_button = ttk.Button(self.root, text="Iniciar", command=self.start_detection)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root, text="Detener", command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.zone_labels = []
        self.zone_labels_text = []
        for i in range(7):
            label_text = tk.StringVar() 
            label_text.set(f"Zona {i+1}: 0")
            zone_label = ttk.Label(self.root, textvariable=label_text)
            zone_label.pack()
            self.zone_labels.append(zone_label)
            self.zone_labels_text.append(label_text)

        self.show_graph_button = ttk.Button(self.root, text="Mostrar Gráficas", command=self.show_graphs)
        self.show_graph_button.pack(pady=10)

    def start_detection(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        threading.Thread(target=self.detect_people).start()

    def stop_detection(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        self.cap.release()

    def detect_people(self):
        detector(self.cap)
        #va = get_detection()

        #for i, label in enumerate(self.zone_labels_text, start=0):
        #    label.set(f"Zona {i+1}: {va[i]}")



    def show_graphs(self):
        # Agregar código para mostrar las gráficas
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonDetectionApp(root)
    root.mainloop()
