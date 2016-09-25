#encoding: utf-8

#import sys
#sys.modules[__name__].__dict__.clear()
import cv2
import matplotlib.pyplot as plt
from pylab import *
import numpy as np
from numpy import newaxis
import math

#tomar videos con la mismas dimensiones en X y en Y
capture = cv2.VideoCapture("camilo_mov2.mp4")

#Obtener ancho y alto del video
anchoV = capture.get(3)
anchoV1 = int(anchoV)
altoV = capture.get(4)
altoV1 = int(altoV)
print 'ancho' , anchoV1
print 'alto' , altoV1

#Fotogramas por segundo
frameRateO = capture.get(5)

#Numero de Frames
numFrames = capture.get(7)
numFrames1 = int(numFrames) #Pasandolo de float a Int
print 'Numero de Frames', numFrames1

I = np.zeros(shape =(altoV1,anchoV1,numFrames1))
canal_R = np.zeros(shape = (altoV1, anchoV1), dtype = np.uint8)
canal_G = np.zeros(shape = (altoV1, anchoV1), dtype = np.uint8)
canal_B = np.zeros(shape = (altoV1, anchoV1), dtype = np.uint8)

for iii in xrange(1,numFrames1):

	estado,videoOriginal= capture.read(iii) #leer video para el numero de frames
	tam_video = videoOriginal.shape #tamaño del video (Px,Py,fr)
		
	#Multiplicar Canal R-G-B para pasar a escala de grises
	canal_B = videoOriginal[:,:,0] * 0.114
	canal_G = videoOriginal[:,:,1] * 0.587
	canal_R = videoOriginal[:,:,2] * 0.299

	I[:,:,iii] = canal_R + canal_G + canal_B

	gris_video = I[:,:,iii]
	
	#cv2.imshow('Video Preprocesado', gris_video.astype(np.uint8))  
	#if 0xFF & cv2.waitKey(300) == 3:
	#	break

	pass

################################################################################################################################

#SIGMA DELTA

N = 3
M = np.zeros(shape = (I.shape[0] , I.shape[1] , I.shape[2]), dtype = np.int16)
delta = np.zeros(shape = (I.shape[0] , I.shape[1] , I.shape[2]), dtype = np.int16)
varianza = np.zeros(shape = (I.shape[0] , I.shape[1] , I.shape[2]), dtype = np.int16)
mascara = np.zeros(shape = (I.shape[0] , I.shape[1] , I.shape[2]), dtype = np.int16)
reproducir = np.zeros(shape = (videoOriginal.shape[0] , videoOriginal.shape[1] , videoOriginal.shape[2]))

M[:,:,1] = I[:,:,1] 

for ii in xrange(1,numFrames1-1):

	M[:,:,ii+1] = M[:,:,ii] + np.sign(I[:,:,ii+1] - M[:,:,ii])

	delta[:,:,ii+1] = abs(M[:,:,ii+1] - I[:,:,ii+1])

	if (ii==1):
		varianza[:,:,ii] = delta[:,:,ii]
		pass

	varianza[:,:,ii+1] = varianza[:,:,ii] + np.sign((delta[:,:,ii+1] * N) - varianza[:,:,ii])
	
	mascara[:,:,ii+1] = delta[:,:,ii+1] > varianza[:,:,ii+1]

	reproducir = mascara[:,:,ii+1]
	#cv2.imshow('Deteccion de Movimiento', bool.reproducir)
	#if 0xFF & cv2.waitKey(80) == 1:
	#	break
	
	pass
	
#######################################################################################################

#PRIMERA SUMATORIA DE PERFILES X y Y

xs = np.zeros(shape =(mascara.shape[0] , mascara.shape[2]))
ys = np.zeros(shape =(mascara.shape[1] , mascara.shape[2]))

xSuma = np.sum(mascara,1)
ySuma = np.sum(mascara,0)

xs[:,:] = xSuma[:,:]
ys[:,:] = ySuma[:,:]

xmax = np.max(xs[:,:],0)
ymax = np.max(ys[:,:],0)

######################################################################################################

# IMAGEN PERFILES

xn = np.zeros(shape = (xs.shape))
yn = np.zeros(shape = (ys.shape))

xFullmax = np.max(xmax)
yFullmax = np.max(ymax)

xn = xs[:,:] / xFullmax
yn = ys[:,:] / yFullmax

plot(xn)
cv2.destroyAllWindows()
