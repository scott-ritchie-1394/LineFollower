#!/usr/bin/env python
from __future__ import print_function
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from picamera.array import PiRGBArray
from PiVideoStream import PiVideoStream
from picamera import PiCamera
import numpy as np
import serial
import os.path
import time
import imutils
import cv2
import io
import spidev

drive = 16
angle = 0

spi = spidev.SpiDev()
spi.open(0,0)
width = 640
height = 480
Kp = .3984 * 1.25 
Kd = 2
dt = 128
it = 0
Ki = 0 
horLine = 300
colors = [[0,0,0],[255,0,0],[0,255,0],[0,0,255],[255,255,0],[255,0,255],[0,255,255],[255,255,255],[0,0,0]]
def convertToBits(number):
	bits = []
	testers = [128,64,32,16,8,4,2,1]
	for x in range(0,8):
		if number & testers[x] == 0:
			bits.append(0)
		else:
			bits.append(1)
	return bits
def findCenter(vs):
	imgc = vs.read()
	imgc = cv2.GaussianBlur(imgc,(1,1),0)
	img = cv2.cvtColor(imgc,cv2.COLOR_BGR2GRAY)
	thresh1 = cv2.threshold(img,200,255,cv2.THRESH_BINARY)
	count = 0
	sum = 0
	for y in range(0,width):
		if thresh1[1][horLine][y] == 255:
			count += 1
			sum += y
		y += 1
	if count != 0:
		avg = int(sum / count)
	else:
		avg = -1
		return
	PD(avg - (width/2))
	#steer(PD(avg - (width/2)))
def PD(error_orig):
	global dt,it
	error = 0
	if(error_orig < 0):
		error = error_orig - 40
	else:
		error = error_orig + 20
	Pvalue = int(round(Kp*error + 127.5))
	if(Pvalue < 0):
		Pvalue = 0
	if(Pvalue > 255):
		Pvalue = 254
	Dvalue = int(round(Kd * ((Pvalue) - dt)))
	it = it + Pvalue
	if it > 255:
		it = 254
	elif it < 0:
		it = 0
	dt = Pvalue
	Ivalue = it * Ki
	PD = Pvalue + Dvalue + int(round(Ivalue))
	if(PD < 0):
		PD = 0
	if(PD > 255):
		PD = 254
	#print("PVAL: " + str(Pvalue) + ", DVAL: " + str(Dvalue) + ", PD: " + str(PD))
	steer(PD)
	return PD 
def steer(ste):
	spi.xfer([angle,ste])
vs = PiVideoStream().start()
time.sleep(2.0)
myCount = 0
spi.xfer([drive,50])
time.sleep(.1)
spi.xfer([drive,119])
start = time.time()
toModulate = 1
while myCount < 500:
	if(toModulate % 5 == 0):
		spi.xfer([drive,128])
		toModulate = 1
	else:
		spi.xfer([drive,119])
	findCenter(vs)
	myCount += 1
	toModulate = toModulate + 1
print("FPS: " + str(500/(time.time() - start)))
spi.xfer([angle,128])
spi.xfer([drive,128])
vs.stop() 
