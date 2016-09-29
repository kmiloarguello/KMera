#encoding: utf-8

#import sys
#sys.modules[__name__].__dict__.clear()
import cv2
import matplotlib.pyplot as plt
from matplotlib.mlab import PCA
from scipy import linalg
from pylab import *
import numpy as np
from numpy import newaxis , mean ,cov ,double,cumsum,dot,linalg,array,rank
import math

#tomar videos con la mismas dimensiones en X y en Y
capture = cv2.VideoCapture('camilo_mov3.mp4')

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
#numFrames1 = 10
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
	#if 0xFF & cv2.waitKey(30) == 3:
	#	break

	pass

################################################################################################################################

#SIGMA DELTA

N = 3
Ms = np.zeros(shape = (I.shape[0] , I.shape[1] , I.shape[2]), dtype = np.int16)
delta = np.zeros(shape = (I.shape[0] , I.shape[1] , I.shape[2]), dtype = np.int16)
varianza = np.zeros(shape = (I.shape[0] , I.shape[1] , I.shape[2]), dtype = np.int16)
mascara = np.zeros(shape = (I.shape[0] , I.shape[1] , I.shape[2]), dtype = np.int16)
reproducir = np.zeros(shape = (videoOriginal.shape[0] , videoOriginal.shape[1] , videoOriginal.shape[2]))

Ms[:,:,1] = I[:,:,1] 

for ii in xrange(1,numFrames1-1):

	Ms[:,:,ii+1] = Ms[:,:,ii] + np.sign(I[:,:,ii+1] - Ms[:,:,ii])

	delta[:,:,ii+1] = abs(Ms[:,:,ii+1] - I[:,:,ii+1])

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
	
################################################################################################################################

#PRIMERA SUMATORIA DE PERFILES X y Y

xs = np.zeros(shape =(mascara.shape[0] , mascara.shape[2]))
ys = np.zeros(shape =(mascara.shape[1] , mascara.shape[2]))

xSuma = np.sum(mascara,1)
ySuma = np.sum(mascara,0)

xs[:,:] = xSuma[:,:]
ys[:,:] = ySuma[:,:]

xmax = np.max(xs[:,:],0)
ymax = np.max(ys[:,:],0)

################################################################################################################################

# IMAGEN PERFILES

xn = np.zeros(shape = (xs.shape))
yn = np.zeros(shape = (ys.shape))

xFullmax = np.max(xmax)
yFullmax = np.max(ymax)

xn = xs[:,:] / xFullmax
yn = ys[:,:] / yFullmax

'''
#Ploteando Imagenes 
plt.subplot(1,2,1)
plt.imshow(xn, interpolation='nearest')

plt.subplot(1,2,2)
plt.imshow(yn, interpolation='nearest')
show()
'''

################################################################################################################################

# PCA 

Ts = 1 / frameRateO

def princomp(yn):

 M = (yn-mean(yn.T,axis=1)).T # subtract the mean (along columns)
 [latent,coeff] = linalg.eig(cov(M)) # attention:not always sorted
 score = dot(coeff.T,M) # projection of the data in the new space
 return coeff,score,latent

coeff, score, latent = princomp(yn)

xMean = mean(coeff[:,0])
centroPcax = xMean - coeff[:,0]
## FALTA DEJAR EJE X EN SEGUNDOS :)

figure(1)
plt.plot(centroPcax)
plt.show()

################################################################################################################################

# Analisis Frecuencial

Fs = 1 / Ts

magxF = abs(np.fft.fft(centroPcax))
magxF = np.fft.fftshift(magxF)

f_esp = Fs / len(centroPcax)
f_inicial = -(Fs / 2)
f_final = (Fs / 2) 

fr = np.arange(f_inicial, f_final, f_esp)

print 'btw', f_esp
print 'Fs', f_final
print 'y',magxF.shape
print 'x',fr.shape

figure(2)
plt.plot(fr,magxF)
title('Single-sided amplitude spectrum of y(t)')
xlabel('Frequency (Hz)')
ylabel('|Y(f)|')
plt.show()


'''
#ERRORES CON PCA POR CORREGIR
#xnan=np.isnan(xn)

def prinCompoAnalisis(yn):
 # computing eigenvalues and eigenvectors of covariance matrix
 pca_Meanx = (xn-mean(xn.T,axis=1)).T # subtract the mean (along columns)
 pca_Meany = (yn-mean(yn.T,axis=1)).T

 [latentx , coeffx] = linalg.eig(cov(pca_Meanx)) # attention:not always sorted
 [latenty , coeffy] = linalg.eig(cov(pca_Meany)) 

 scorex = dot(coeffx.T , pca_Meanx) # projection of the data in the new space
 scorey = dot(coeffy.T , pca_Meany)

 return coeffx,coeffy,scorex,scorey,latentx,latenty

coeffx , scorex , latentx = prinCompoAnalisis(xn.T)
coeffy , scorey , latenty = prinCompoAnalisis(yn.T)

figure()

plt.plot(coeffx[:,4])
plt.show()

subplot(121)
# every eigenvector describe the direction
# of a principal component.
m = mean(xn,axis=1)
plot([0, -coeff[0,0]*2]+m[0], [0, -coeff[0,1]*2]+m[1],'--k')
plot([0, coeff[1,0]*2]+m[0], [0, coeff[1,1]*2]+m[1],'--k')
plot(xn[0,:],xn[1,:],'ob') # the data
axis('equal')
subplot(122)
# new data
plot(score[0,:],score[1,:],'*g')
axis('equal')
show()
-----------------------------------------------------------------------------------------
#ANALISIS FRECUENCIAL

#which = magxF[1:].argmax() + 1 #indice maximo en Frecuencia


def frange(inicio, final, btween):
	i = inicio
	while (i < final):
		yield i
		i += between

#L  = len(coeff[:,0])
#tiempo  = arange(0,L)*Ts
#x  = 0.7*sin(2*pi*50*t)+sin(2*pi*120*t)
#y  = x + 2*randn(len(t))
#plot(Fs*t[:50],y[:50])
#title('Signal corrupted with zero-mean random noise')
#xlabel('Time (milliseconds)')
'''

capture.release()
cv2.destroyAllWindows()