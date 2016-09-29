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
from Tkinter import *
import random
import time
import pygame

#tomar videos con la mismas dimensiones en X y en Y
capture = cv2.VideoCapture('soccer.avi')

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

capture.release()
cv2.destroyAllWindows()
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

t_prueba1 = 1 / indicex
t_prueba2 = 1 / indicey
To_segx = Tox * Ts
To_segy = Toy * Ts

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

# GENERACION DE BEAT 1

fs_sound = 48000
fs_step = 1.0 / fs_sound
tseno = np.arange(0,0.1,fs_step)
s_seno = np.sin(2*(np.pi)*440*tseno)

d_sound = numFrames1 *  Ts

frq_beatx = t_prueba1 
frq_beaty = t_prueba2 

fs_step = 1.0 / fs_sound 
t_video = np.arange(0,d_sound,fs_step)

y_impulsox = np.zeros(shape = (t_video.shape))
y_impulsoy = np.zeros(shape = (t_video.shape))

imp_soundx = np.around( (fs_sound / frq_beatx)) 
imp_soundy = np.around( (fs_sound / frq_beaty) * 2)

y_impulsox[1::imp_soundx] = 1
y_impulsoy[1::imp_soundy] = 1

sound_convx = np.convolve(s_seno,y_impulsox,'same')
sound_convy = np.convolve(s_seno,y_impulsoy,'same')

print imp_soundy

write('beat.wav', fs_sound, sound_convx)
write('beat.wav', fs_sound, sound_convy)

################################################################################################################################

#GAME _ primera Iteración
'''
pygame.init()
pygame.mixer.init()
sounda = pygame.mixer.Sound("beat1.wav")
sounda.play()
time.sleep (20)
'''
size_canvax = 500
#vel_pelota = size_canvax / (t_prueba1 * frameRateO)
vel_pelota = 5


class Pelota(object):
	def __init__(self, canvas,color):
		self.canvas = canvas
		self.id = canvas.create_oval(10,10,25,25,fill = color) #creacion bolita
		self.canvas.move(self.id,250, 0) #Posicion bolita
		self.x = 0 #velocidad x
		self.y = -vel_pelota #velocidad y --- px / fr
		self.canvas_height = self.canvas.winfo_height()

	def dibujar(self):
		self.canvas.move(self.id,self.x,self.y)
		pos = self.canvas.coords(self.id)
		if (pos[1] <= 0):
			self.y = vel_pelota
		if (pos[3] >= self.canvas_height):
			self.y = -vel_pelota

tk = Tk()
tk.title("Camilo App")
tk.resizable(0,0)
tk.wm_attributes("-topmost",1)
canvas = Canvas(tk, width = size_canvax, height = size_canvax, bd = 0, highlightthickness = 0)
canvas.pack()
tk.update()

pelota = Pelota(canvas,'black')

while 1:
	pelota.dibujar()
	tk.update_idletasks()
	tk.update()
	time.sleep(0.01)


##resultados


figure(1)
plt.subplot(1,2,1)
plt.imshow(xn, interpolation='nearest')

plt.subplot(1,2,2)
plt.imshow(yn, interpolation='nearest')
#plt.show()

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

