#encoding: utf-8
import cv2
import matplotlib as plt
import numpy as np
from numpy import newaxis
import math

capture = cv2.VideoCapture("colors.avi")

#Obtener ancho y alto del video
anchoV = capture.get(3)
anchoV1 = int(anchoV)
altoV = capture.get(4)
altoV1 = int(altoV)
#print 'ancho' , anchoV1
#print 'alto' , altoV1

#Fotogramas por segundo
frameRateO = capture.get(5)

#Numero de Frames
numFrames = capture.get(7)
numFrames1 = int(numFrames) #Pasandolo de float a Int
#print 'Numero de Frames', numFrames1

#I=np.array([4,5,6])
#print I


for iii in xrange(1,numFrames1):
	estado,videoOriginal= capture.read(iii) #leer video para el numero de frames
	tam_video = videoOriginal.shape #tamaño del video (Px,Py,fr)
	I = np.zeros(shape =(tam_video[0],tam_video[1],iii))
	#Multiplicar Canal R-G-B para pasar a escala de grises
	
	canal_R = videoOriginal[:,:,0] * 0.299 
	canal_G = videoOriginal[:,:,1] * 0.587
	canal_B = videoOriginal[:,:,2] * 0.114

	#I[tam_video[0],tam_video[1],iii] = canal_R + canal_G + canal_B

	#img = I[:,:, newaxis]
	
	#I = cv2.cvtColor(videoOriginal, cv2.COLOR_BGR2GRAY) #Conversion a escala de grises
	'''
	cv2.imshow('Ventana de Video', videoOriginal)  
	if 0xFF & cv2.waitKey(3) == 27:       
	   break
	'''
	pass

print I
print I.shape




##################################################################################################################

#SIGMA DELTA
'''
N = 3
tam_I = I.shape
M = np.zeros(tam_I[0],tam_I[1],tam_I[2])
M[:,:,1] = I[:,:,1] 

for ii in xrange(1,numFrames1-1):
	
	if (M[:,:,ii]<I[:,:,ii+1]):
		M[:,:,ii+1] = M[:,:,ii]+1
		pass
	elif (M[:,:,ii]>I[:,:,ii+1]):
		M[:,:,ii+1] = M[:,:,ii]-1
		pass
	else:
		M[:,:,ii+1] = M[:,:,ii]
	pass

	delta[:,:,ii+1] = abs(M[:,:,ii+1] - I[:,:,ii])

	if (ii==1):
		varianza[:,:,ii] = delta[:,:,ii]
		pass

	while (delta[:,:,ii+1] != 0:

		if (varianza[:,:,ii] < (N * delta[:,:,ii+1])):
			varianza[:,:,ii+1] = varianza[:,:,ii] + 1
			pass
		elif (varianza[:,:,ii] > (N * delta[:,:,ii+1])):
			varianza[:,:,ii+1] = varianza[:,:,ii] - 1
			pass
		else: 
			varianza[:,:,ii+1] = varianza[:,:,ii]

	mascara[:,:,ii+1] = delta[:,:,ii+1] > varianza[:,:,ii+1]

pass

#######################################################################################################

#PRIMERA SUMATORIA DE PERFILES X y Y
tam_mascara = mascara.shape
xs = np.zeros(shape =(mascara[0],mascara[2]))
ys = np.zeros(shape =(mascara[1],mascara[2]))

xSuma = sum(mascara,2)
ySuma = sum(mascara,1)

xs[:,:] = xSuma[:,1,:]
ys[:,:] = ySuma[1,:,:]

'''
cv2.destroyAllWindows()
