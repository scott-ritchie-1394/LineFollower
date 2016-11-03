#!/usr/bin/env python
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
import io

Kp = .3984 *2
Kd = 0
dt = 0
strait = 160
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
def findCenter(camera):
	stream = io.BytesIO()
	camera.capture(stream, format='jpeg',use_video_port=True)
	data = np.fromstring(stream.getvalue(), dtype=np.uint8)
	imgc = cv2.imdecode(data,1)
	imgc = cv2.GaussianBlur(imgc,(3,3),0)
	img = cv2.cvtColor(imgc,cv2.COLOR_BGR2GRAY)
	thresh1 = cv2.threshold(img,200,255,cv2.THRESH_BINARY)
	count = 0
	sum = 0
	for y in range(0,640):
		imgc[horLine][y] = colors[1]
		if thresh1[1][horLine][y] == 255:
			count += 1
			sum += y
		y += 1
	if count != 0:
		avg = int(sum / count)
	else:
		avg = -1
		return
	x = 0
	for x in range(0,480):
		imgc[x][avg] = colors[1]
		x += 1
	PD(avg - 480/2)
	cv2.imshow("image",imgc)
	#cv2.imshow("thresh",thresh1[1])
	cv2.waitKey(0)
def PD(error_orig):
	error = 0
	if(error_orig < 0):
		error = error_orig - 30
	else:
		error = error_orig + 20
	Pvalue = int(round(Kp*error + 127.5))
	Dvalue = Kd * (error - dt)
	PD = Pvalue + Dvalue
	print(PD)
	return PD 
with PiCamera() as camera:
	camera.resolution = (640,480)
	myCount = 0
	while myCount < 50:
		startTotal = time.time()
		findCenter(camera)
		myCount += 1 
