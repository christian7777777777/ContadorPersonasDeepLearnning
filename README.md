# Contador Personas  Deep Learning con Python
Proyecto de Deep Learnning con Python para detectar y contar personas con YOLO de Ultralytics
Este proyecto utiliza técnicas de visión por computadora y aprendizaje profundo para detectar y contar personas en un video en tiempo real. Utiliza el modelo YOLOv5 para la detección de personas y el algoritmo SORT para el seguimiento de objetos.

# Instalación
1. Clona este repositorio en tu máquina local: https://github.com/christian7777777777/ContadorPersonasDeepLearnning.git
2. Instala las dependencias necesarias: pip install -r requirements.txt

# Uso
1. Ejecuta el archivo "GUI.py" y se desplegara la interfaz Grafica de Usuario(GUI) Principal, podras visualizar en la parte superior-izquierda, dos botones; "Iniciar" para empezar con la deteccion y "Detener" para detener el proceso de deteccion. Procurar tener instalado las librerias necesarias para correr el codigo y editar el PATH del video en funcion del directorio donde se haya clonado el proyecto.
3. Debajo de los botones vizualizaras 7 Etiquetas en las cuales se mostraran las metricas de conteo de las predicciones del video, tambien podras ver las metricas dentro del video mismo.
4. Debajo de las etiquetas, estaran un ComboBox el cual contiene las opciones para graficar resultados. Importante saber que esta seccion solo es valida cuando ya se ha detenido el proceso de Deteccion. Solo una vez detenido el proceso de deteccion se hablilitara el boton "Graficar"
5. En la parte derecha de la GUI se visualizara un label donde se mortrara el video una vez iniciado el proceso y debajo de este un Axis para las graficas.
6. Para visualizar las graficas, elejir una opcion del ComboBox(Por defecto ewsta en "Valores maximos de aglomeracion por zona") y presionar "Graficar", Importante hacerlo una vez detenido el proceso de Deteccion. Para cerrar El programa solo dar click en la "X" de la Ventana Principal.
7. Para mejor comprension revisar este video exlicativo: https://youtu.be/nIhCFL6hDeI

# Caracteristicas
* Detección y seguimiento de personas en tiempo real.
* Conteo de personas por zonas predefinidas en el video.
* Visualización de métricas de conteo en una interfaz gráfica de usuario (GUI).
* Generación de gráficas de aglomeración global y por zonas.

# Contribución
Si quieres contribuir a este proyecto, por favor sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una nueva rama con tu funcionalidad: git checkout -b feature/nueva-funcionalidad.
3. Haz tus cambios y commitea: git commit -am 'Agrega una nueva funcionalidad'.
4. Push a la rama: git push origin feature/nueva-funcionalidad.
5. Crea un pull request en GitHub.

# Creditos
* Desarrollado por Christian M. Oyaque.
* Basado en el modelo YOLOv5 de Ultralytics.
* Utiliza el algoritmo SORT de Alex Bewley alex@bewley.ai
   
