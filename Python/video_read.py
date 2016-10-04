#Programa para cargar el video y preprocesarlo
#encoding: utf-8
################################################
################################################

# 1. Importar librerias

#import numpy 
import cv2 #Importamos la libreria de OpenCV


###################################################
###################################################

# 2. cargar el video

#llama clase videocapture de la libreria cv2
capture = cv2.VideoCapture("camilo_mov2.mp4") #Creamos una variable en donde almacenamos
# los datos que se leen del archivo de video


##################################################
##################################################

# 3. Procesamiento

while True: #Realizamos una lectura continua del archivo de video
    ret, img = capture.read()              #Leemos cada uno de los fotogramas del archivo de video
    cv2.imshow('Ventana de Video', img)    #Mostramos los fotogramas en una ventana
    if 0xFF & cv2.waitKey(5) == 10:        #Si se presiona la tecla ESC el video se detiene
                                          #Si no se pone un valor en waitkey, se 1 frame a la vez, por defecto está 5
       break
#retorna un booleano, si el frame es correcto -> verdadero.
#cuando no se inicializa cap, se verifica con "cap.isOpened()" si esta bien, sino usar "cap.open()".
#para tener mas herramientas de este video usar el método"cap.get(propId)".
#propId es un numero entre  y 18, c/numero denota una propiedad del video


#################################################
#################################################
# 4. Mostrar el video

cv2.destroyAllWindows() #Cerras las ventanas para liberar memoria