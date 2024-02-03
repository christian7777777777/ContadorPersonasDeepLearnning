import tkinter as tk
import cv2
import torch
import numpy as np 
import matplotlib.path as mplPath
from sort import Sort

class ContadorPersonas():

    def __init__(self):
        self.zonas = [
            np.array([[3,236],[3,184],[298,212],[288,291]]),
            np.array([[532,184],[692,222],[762,150],[762,97],[727,93]]),
            np.array([[694,232],[555,400],[761,479],[760,302]]),
            np.array([[2,251],[290,310],[476,386],[744,509],[742,561],[8,558]]),
            np.array([[2,168],[4,145],[236,98],[648,122],[550,167],[459,190],[300,200]]),
            np.array([[313,214],[304,293],[542,389],[668,231],[520,192]]),
            np.array([[4,76],[2,136],[240,86],[297,70],[278,43],[207,38]])
            ]
        self.deteccion_zona = [0, 0, 0, 0, 0, 0, 0]
   
    def load_model(self):
        model = torch.hub.load("ultralytics/yolov5", model="yolov5n", pretrained=True)
        return model

    def get_bdoxes(self, preds: object):
        df = preds.pandas().xyxy[0]
        df = df[df["confidence"] >= 0.5]
        df = df[df["name"] == "person"]

        return df[["xmin", "ymin", "xmax", "ymax"]].values.astype(int)

    def get_center(self, bbox):
        #xmin, ymin, xmax, ymax
        # 0     1     2     3
        center = ((bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2)
        return center

    def get_center_zona(self, poligon):

        center = (int(np.mean(poligon[:, 0])-50), int(np.mean(poligon[:, 1])))
        return center

    def is_valid_detection(self, xc, yc, zona):
        return mplPath.Path(zona).contains_point((xc, yc))
    
    def detector(self, cap: object):
  
        model = self.load_model()
        tracker = Sort()

        while cap.isOpened():
            status, frame = cap.read()

            if not status:
                break
            
            preds = model(frame)
            bboxes = self.get_bdoxes(preds)
            
            tracks = tracker.update(bboxes)
            tracks = tracks.astype(int)

            self.deteccion_zona =[0, 0, 0, 0, 0, 0, 0]

            for box in tracks:
                xc, yc = self.get_center(box)
                for i, zona in enumerate(self.zonas, start=0):
                    if self.is_valid_detection(xc, yc, zona):
                        self.deteccion_zona[i] += 1

                cv2.circle(img=frame, center=(xc, yc), radius=5, color=(0,255,0), thickness=-1)
                cv2.putText(img=frame, text=f"Id: {box[4]}", org=(box[0], box[1]-10), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(0,255,0), thickness=2)
                cv2.rectangle(img=frame, pt1=(box[0], box[1]),pt2=(box[2], box[3]), color=(255, 0, 0), thickness=2)

            for i, zona in enumerate(self.zonas, start=1):
                x_center, y_center = self.get_center_zona(zona)
                cv2.polylines(img=frame, pts=[zona], isClosed=True, color=(0, 0, 255), thickness=2)
                cv2.putText(img=frame, text=f"Zona{i}: {self.deteccion_zona[i-1]}", org=(x_center, y_center), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(255, 255, 255), thickness=2)

            cv2.imshow("frame", frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()


#if __name__ == '__main__':
#    cap = cv2.VideoCapture(r"C:\Users\User\OneDrive\Escritorio\proyecto-20240121T230321Z-001\proyecto\video.webm")
#    ventana = ContadorPersonas()

#    ventana.detector(cap)
