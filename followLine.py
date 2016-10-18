#!/usr/bin/env python
from __future__ import print_function
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from picamera.array import PiRGBArray
from PiVideoStream import PiVideoStream
from picamera import PiCamera
import numpy as np
import time
import imutils
import cv2
import io


width = 640
height = 480
Kp = 2
Kd = 1
dt = 0
horLine = 380
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
	img = cv2.cvtColor(imgc,cv2.COLOR_BGR2GRAY)
	thresh1 = cv2.threshold(img,150,255,cv2.THRESH_BINARY)
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
	PD(avg - (width/2))
def PD(error):
	Pvalue = Kp*error
	Dvalue = Kd * (error - dt)
	PD = Pvalue + Dvalue
	return PD 
vs = PiVideoStream().start()
time.sleep(2.0)
myCount = 0
startLoop = time.time()
while myCount < 100:
	findCenter(vs)
	myCount += 1
print(str(100/(time.time() - startLoop)) + " FPS")
vs.stop() 
