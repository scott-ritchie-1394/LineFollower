#!/usr/bin/env python
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
import io

Kp = 2
Kd = 1
dt = 0
horLine = 200
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
def findCenter(camera,stream):
	start = time.time()
	#stream = io.BytesIO()
	camera.capture(stream, format='bgr',use_video_port=True)
	data = np.fromstring(stream.getvalue(), dtype=np.uint8)
	print("Capture time: " + str(time.time() - start))
	imgc = stream.array
	img = cv2.cvtColor(imgc,cv2.COLOR_BGR2GRAY)
	thresh1 = cv2.threshold(img,150,255,cv2.THRESH_BINARY)
	count = 0
	sum = 0
	for y in range(0,320):
		if thresh1[1][horLine][y] == 255:
			count += 1
			sum += y
		y += 1
	if count != 0:
		avg = int(sum / count)
	else:
		avg = -1
	PD(avg - 160)
def PD(error):
	Pvalue = Kp*error
	Dvalue = Kd * (error - dt)
	PD = Pvalue + Dvalue
	return PD 
with PiCamera() as camera:
	with PiRGBArray(camera) as stream:
		camera.resolution = (320,240)
		myCount = 0
		while myCount < 100:
			startTotal = time.time()
			findCenter(camera,stream)
			stream.truncate(0)
			print("Time = " + str(time.time() - startTotal))
			myCount += 1 
