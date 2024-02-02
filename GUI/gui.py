import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading


class VideoApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.canvas = tk.Canvas(window, width=800, height=600)
        self.canvas.pack()
        
        self.btn_start = tk.Button(window, text="Start", width=10, command=self.start_detection_thread)
        self.btn_start.pack(anchor=tk.CENTER, expand=True)
        
        self.btn_stop = tk.Button(window, text="Stop", width=10, command=self.stop_detection)
        self.btn_stop.pack(anchor=tk.CENTER, expand=True)
        
        self.detection_thread = None
        self.is_detection_running = False

        self.delay = 10
        self.update()

        self.window.mainloop()

    def start_detection_thread(self):
        if not self.is_detection_running:
            self.is_detection_running = True
            self.detection_thread = threading.Thread(target=self.start_detection)
            self.detection_thread.start()

    def stop_detection(self):
        if self.is_detection_running:
            self.is_detection_running = False
            self.detection_thread.join()
            self.video_capture.release()

    def start_detection(self):
        messagebox.showinfo("Mensaje", "El proceso YOLO está comenzando...")


        self.video_capture.release()

    def update(self):
        if not self.is_detection_running:
            return
        
        self.window.after(self.delay, self.update)

# Ejemplo de uso:
if __name__ == "__main__":
    window = tk.Tk()
    app = VideoApp(window, "Interfaz Gráfica con YOLO")
