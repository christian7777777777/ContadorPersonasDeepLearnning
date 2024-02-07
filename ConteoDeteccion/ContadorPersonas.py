import tkinter as tk                #Libreria para GUI
import cv2                          #Libreria para captura de Video
import torch                        #Libreria para carga y desplige de Modelo YOLO
import numpy as np                  #Libreria para manejo de matrices
import matplotlib.path as mplPath   #Libreria para graficas
from sort import Sort               #Libreria para Tracking
import imutils                      #Librerias para redimencionar el video
from PIL import Image, ImageTk      #Libreria para convertir frame en Imagen

class ContadorPersonas():

    def __init__(self):
        
        #Constructor con variables de clase ContadorPersonas(), Zonas de deteccion predefinidas y lista de Detecciones (Vacia)
        self.zonas = [
            np.array([[3,236],[3,184],[298,212],[288,291]]),
            np.array([[532,184],[692,222],[762,150],[762,97],[727,93]]),
            np.array([[694,232],[555,400],[761,479],[760,302]]),
            np.array([[2,251],[290,310],[476,386],[744,509],[742,561],[8,558]]),
            np.array([[2,168],[4,145],[236,98],[648,122],[550,167],[459,190],[300,200]]),
            np.array([[313,214],[304,293],[542,389],[668,231],[520,192]]),
            np.array([[4,76],[2,136],[240,86],[297,70],[278,43],[207,38]])
            ]
        self.ListaDetecciones = []
    
    #Metodo para cargar modelo de Deteccion (YOLO)
    def load_model(self):
        model = torch.hub.load("ultralytics/yolov5", model="yolov5n", pretrained=True)
        return model

    #Metodo para obtener los Bbox de cada deteccion
    def get_bdoxes(self, preds: object):
        df = preds.pandas().xyxy[0]
        df = df[df["confidence"] >= 0.5]    #Establecemos un nivel de confianza de deteccion de 50%
        df = df[df["name"] == "person"]     #Filtramos detecciones a personas

        return df[["xmin", "ymin", "xmax", "ymax"]].values.astype(int)  #Retorna bbox de detecciones

    #Metodo para Obtener el centro del Bbox de deteccion que ayudara en el conteo de personas por zona
    def get_center(self, bbox):
        #xmin, ymin, xmax, ymax
        # 0     1     2     3
        center = ((bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2)
        return center   #retorna tupla (xc, yc)

    #Metodo para obtener el centro de zona para poder mostrar metrias de conteo
    def get_center_zona(self, poligon):

        center = (int(np.mean(poligon[:, 0])-50), int(np.mean(poligon[:, 1])))
        return center   #retorna tupla (xc, yc)

    #Metodo para detectar si el centro de un Bbox Detectado estan dentro de una zona(poligono)
    def is_valid_detection(self, xc, yc, zona):
        #Pasamos como parametros, el centro del Bbox de personas detectada y el Poligino de Zona
        return mplPath.Path(zona).contains_point((xc, yc))
    
    #Metodo para Deteccion y conteo de Personas en zonas determinadas
    def detector(self, cap: object, lblVideo: tk, lblDetecciones: list):
        #Parametros:
        #   Cap -> VideoCaputure()
        #   lblVideo -> Label para mostrar frame por frame en GUI 
        #   lblDetecciones -> lista de StringVar a ser modificadas con metricas de conteo 
  
        model = self.load_model()   #Cargar modelo
        tracker = Sort()            #Utilizacion de Sort() para seguimiento de Bbox (Tracking)

        #Ciclo de Frames del Video
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            #Predicciones con Modelo Cargado
            preds = model(frame)

            #Utilizacion Metodo para obtener Bbox de Detecciones
            bboxes = self.get_bdoxes(preds)
            
            #Sort solo necesita Bbox para realizar el Tracking del Objeto y me retorna su id
            tracks = tracker.update(bboxes)
            tracks = tracks.astype(int)     #[xmin, xmax, ymin, ymax, id]


            #Variable auxiliar para redicciones de cada frame
            deteccion_zona =[0, 0, 0, 0, 0, 0, 0]

            #Ciclo para contar las personas que estan en cada zona con la variable "tracks", es decir con su Id de seguimiento por Sort()
            for box in tracks:
                xc, yc = self.get_center(box)
                for i, zona in enumerate(self.zonas, start=0):
                    if self.is_valid_detection(xc, yc, zona):
                        deteccion_zona[i] += 1

                #Dibujado de detecciones en el frame, asi como su Bbox y Id. 
                cv2.circle(img=frame, center=(xc, yc), radius=5, color=(0,255,0), thickness=-1) #ciculo verde en el centro del Bbox
                cv2.putText(img=frame, text=f"Id: {box[4]}", org=(box[0], box[1]-10), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(0,255,0), thickness=2)
                cv2.rectangle(img=frame, pt1=(box[0], box[1]),pt2=(box[2], box[3]), color=(255, 0, 0), thickness=2)

            #Ciclo para debujar cada zona (Poligono) Pre-Establecida
            for i, zona in enumerate(self.zonas, start=1):
                x_center, y_center = self.get_center_zona(zona)
                cv2.polylines(img=frame, pts=[zona], isClosed=True, color=(0, 0, 255), thickness=2)
                cv2.putText(img=frame, text=f"Zona{i}: {deteccion_zona[i-1]}", org=(x_center, y_center), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(255, 255, 255), thickness=2)  #Metricas de conteo en Frame
                lblDetecciones[i-1].set(f"Personas en Zona {i}: {deteccion_zona[i-1]} Personas")    #Metricas de conteo en labels GUI

            #Agregacion de Lista de detecciones de cada frame a una lista de detecciones en todos los frames que van mostrandose
            #Esto ayudara a realizar las graficas al final del video
            self.ListaDetecciones.append(deteccion_zona)

            #Rendimensionamos el video
            frame = imutils.resize(frame, width=640)

            #Convertimos el video
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            # Mostramos en el GUI
            lblVideo.configure(image=img)
            lblVideo.image = img

            #Condicional para romper el ciclo de frames
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        
        #Metodo para eliminar filas de recgistros de detecciones repetidas
        #   ***IMPORTANTE***
        #   Esto solo es importante para graficar los maximos de detecciones al final del video
        filas_unicas = []
        for fila in self.ListaDetecciones:
            if fila not in filas_unicas:
                filas_unicas.append(fila)
        
        #Convertir Lista de Listas en Matrices para mejor uso de Datos
        self.MatrizDetecciones = np.array(filas_unicas) #Matriz SIN filas repetidas
        self.MatrizDeteccionesCompleta = np.array(self.ListaDetecciones) #Matriz Completa de detecciones en cada Frame (Esta la utlizamos para mostear graficas por zonas)
        
        #Reset de variables y Obtencion de Metodo get_stadistics() Para obtener los maximos de personas por zonas
        self.ListaDetecciones = []
        self.get_stadistics()

        cap.release()

    #Metodo para obtener Maximos de Personas por zonas
    def get_stadistics(self):
        
        #Variables Auxiliares
        MaximoDetecciones = []
        row, column = self.MatrizDetecciones.shape
        
        #ciclo para obtener los maximos de cada columna de la matriz generada anteriormente 
        for j in range(column):
            aux = 0
            for i in range(row):
                if (self.MatrizDetecciones[i][j] > aux):
                    aux = self.MatrizDetecciones[i][j]
            MaximoDetecciones.append(aux)
        return MaximoDetecciones    #Retormanos Vector de Maximos de Personas por cada Zona
    
    #Metodo para Obtener Vector de Detecciones de zona pasada por parametro (zone)
    def get_stadistics_zone(self, zone):
        columna_seleccionada = self.MatrizDeteccionesCompleta[:, zone]
        vector_x = np.arange(1, self.MatrizDeteccionesCompleta.shape[0] + 1)
        vector_y = columna_seleccionada
        return vector_x, vector_y   #Retorna Vector de Frames(vector_x) y vector de Detecciones en cada frame(vector_y) de zona especificada (zone)

