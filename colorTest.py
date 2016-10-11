#!/usr/bin/env python
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import io

colors = [[0,0,0],[255,0,0],[0,255,0],[0,0,255],[255,255,0],[255,0,255],[0,255,255],[255,255,255],[0,0,0]]
def findCenters(camera):
	stream = io.BytesIO()
	camera.capture(stream, format='jpeg',use_video_port=True)
	data = np.fromstring(stream.getvalue(), dtype=np.uint8)
	imgc = cv2.imdecode(data,1)
	img = cv2.cvtColor(imgc,cv2.COLOR_BGR2GRAY)
	thresh1 = cv2.threshold(img,170,255,cv2.THRESH_BINARY)
	count = 0
	sum = 0
	i = 0
	horLine =230
	while i < 9:
		for y in range(0,320):
			imgc[horLine][y] = colors[i]
			if thresh1[1][horLine][y] == 255:
				count += 1
				sum += y
			y += 1
		if count != 0:
			avg = int(sum / count)
		else:
			avg = -1
		x = 0
		for x in range(0,240):
			imgc[x][avg] = colors[i]
			x += 1
		horLine -= 15
		i += 1
		sum = 0
		count = 0
	cv2.imshow("image",imgc)
	cv2.waitKey(0)
with PiCamera() as camera:
	camera.resolution = (320,240)
	findCenters(camera)
