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
import winsound
from scipy.io.wavfile import write
import time, wave, pymedia.audio.sound as sound

#tomar videos con la mismas dimensiones en X y en Y
capture = cv2.VideoCapture('Paso1_izquierda.mp4')

#Obtener ancho y alto del video
anchoV = capture.get(3)
anchoV1 = int(anchoV)
altoV = capture.get(4)
altoV1 = int(altoV)
print 'ancho' , anchoV1
print 'alto' , altoV1

#Fotogramas por segundo
frameRateO = capture.get(5)
print 'frRate',frameRateO

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
	#if 0xFF & cv2.waitKey(30) == 3:
	#	break

	pass

################################################################################################################################

#SIGMA DELTA MOTION DETECTION

N = 3
Ms = np.zeros(shape = (I.shape[0] , I.shape[1] , I.shape[2]), dtype = np.int16)
delta = np.zeros(shape = (I.shape[0] , I.shape[1] , I.shape[2]), dtype = np.int16)
#varianza = np.zeros(shape = (I.shape[0] , I.shape[1] , I.shape[2]), dtype = np.int16)
mascara = np.zeros(shape = (I.shape[0] , I.shape[1] , I.shape[2]), dtype = np.int16)
reproducir = np.zeros(shape = (videoOriginal.shape[0] , videoOriginal.shape[1] , videoOriginal.shape[2]))

Ms[:,:,1] = I[:,:,1] 

for ii in xrange(1,numFrames1-1):

	#Ms[:,:,ii+1] = Ms[:,:,ii] + np.sign(I[:,:,ii+1] - Ms[:,:,ii])
	#delta[:,:,ii+1] = abs(Ms[:,:,ii+1] - I[:,:,ii+1])	
	#if (ii==1):
	#	varianza[:,:,ii] = delta[:,:,ii]
	#	pass
	#varianza[:,:,ii+1] = varianza[:,:,ii] + np.sign((delta[:,:,ii+1] * N) - varianza[:,:,ii])	
	#mascara[:,:,ii+1] = delta[:,:,ii+1] > varianza[:,:,ii+1]

	delta[:,:,ii] = abs(Ms[:,:,1] - I[:,:,ii])
	mascara[:,:,ii] = I[:,:,ii] < delta[:,:,ii] 
	reproducir = delta[:,:,ii]
	'''
	cv2.imshow('Deteccion de Movimiento', reproducir.astype(np.uint8))
	if 0xFF & cv2.waitKey(80) == 1:
		break
	'''
	
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
figure(1)
plt.subplot(1,2,1)
plt.imshow(xn, interpolation='nearest')

plt.subplot(1,2,2)
plt.imshow(yn, interpolation='nearest')
#plt.show()
'''
################################################################################################################################

# PCA 

Ts = 1 / frameRateO

def mypcax(xn):
  Mx = (xn-mean(xn.T,axis=1)).T # subtract the mean (along columns)
  [latentx,coeffx] = linalg.eig(cov(Mx)) # attention:not always sorted
  scorex = dot(coeffx.T,Mx) # projection of the data in the new space
  return coeffx,scorex,latentx

coeffx, scorex, latentx = mypcax(xn)

def mypcay(yn):

 My = (yn-mean(yn.T,axis=1)).T 
 [latenty,coeffy] = linalg.eig(cov(My))
 scorey = dot(coeffy.T,My) 
 return coeffy,scorey,latenty

coeffy, scorey, latenty = mypcay(yn)

xMean = mean(coeffx[:,1])
yMean = mean(coeffy[:,1])

centroPcax = xMean - coeffx[:,1]
centroPcay = yMean - coeffy[:,1]

lon_x = len(centroPcax)
lon_y = len(centroPcay)
tmax_x = (lon_x)*Ts
tmax_y = (lon_y)*Ts
t_x = np.arange(0,tmax_x,Ts)
t_y = np.arange(0,tmax_y,Ts)

'''
figure(2)
plt.subplot(2,1,1)
plt.plot(t_x,centroPcax)
title('Continuos Time signal ')
ylabel('Amplitude X(t)')

plt.subplot(2,1,2)
plt.plot(t_y,centroPcay)
xlabel('Time (Sg)')
ylabel('Amplitude Y(t)')
#plt.show()
'''
################################################################################################################################

# ANALISIS FRECUENCIAL

Fs = 1 / Ts

magxF = abs(np.fft.fft(centroPcax))
magxF = np.fft.fftshift(magxF)
magyF = abs(np.fft.fft(centroPcay))
magyF = np.fft.fftshift(magyF)


f_espx = Fs / len(centroPcax)
f_espy = Fs / len(centroPcay)
f_inicial = -(Fs / 2)
f_final = (Fs / 2) 

frx = np.arange(f_inicial, f_final, f_espx)
fry = np.arange(f_inicial, f_final, f_espy)

#indice maximo en Frecuencia
maximox = np.argmax(magxF)
indicex  = abs(frx[maximox])
maximoy = np.argmax(magyF)
indicey = abs(fry[maximoy])


Fox = indicex * f_espx
Tox = 1 / Fox
Foy = indicey * f_espy
Toy = 1 / indicey

To_segx = Tox * Ts
To_segy = Toy * Ts

#Depronto me muestre To en funcion de los frames y debo compararla con Segundos. #habriaquemirar


'''
figure(3)
plt.subplot(2,1,1)
plt.plot(frx,magxF)
title('Frequency spectrum')
#xlabel('Frequency (Hz)')
ylabel('|X(f)|')

plt.subplot(2,1,2)
plt.plot(fry,magyF)
xlabel('Frequency (Hz)')
ylabel('|Y(f)|')
plt.show()

'''

################################################################################################################################

# GENERACION DE BEAT

#x_sound = wave.open('hard.wav', 'r')
#fs_sound = x_sound.getframerate()
#channels= x_sound.getnchannels()
#frames = x_sound.getnframes()


fs_sound = 48000
fs_step = 1.0 / fs_sound
tseno = np.arange(0,0.1,fs_step)
s_seno = np.sin(2*(np.pi)*440*tseno)
d_sound = numFrames1 *  Ts
frq_beat = Toy
fs_step = 1.0 / fs_sound 
t_video = np.arange(0,d_sound,fs_step)
y_impulso = np.zeros(shape = (t_video.shape))
imp_sound = np.around( fs_sound / frq_beat )
y_impulso[1:imp_sound:] = 1

#format= sound.AFMT_S16_LE
#snd= sound.Output( fs_sound, channels, format )
#s= x_sound.readframes( frames )
#snd.play( s )
#while snd.isPlaying(): time.sleep( 0.05 )

#winsound.PlaySound('worlds.wav', winsound.SND_FILENAME)

sound_conv = np.convolve(y_impulso,s_seno,'same')
#write('beat.wav', 48000, sound_conv)



'''
#data = np.random.uniform(-1,1,44100) # 44100 random samples between -1 and 1
scaled = np.int16(centroPcay/np.max(np.abs(centroPcay)) * 32767)
write('test.wav', 44100, scaled)
'''


capture.release()
cv2.destroyAllWindows()