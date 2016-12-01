#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import sys
import spidev

drive = 16
angle = 0

spi = spidev.SpiDev()
spi.open(0, 0)
#spi.max_speed_hz = 7629

#spi.xfer([angle, 10])
#time.sleep(2)
#spi.xfer([angle, 40])
#time.sleep(2)
#spi.xfer([angle, 70])
#time.sleep(2)
#spi.xfer([angle, 100])
#time.sleep(2)

for i in range(0,255):
    #spi.xfer([angle, i])
    spi.xfer([drive, i])
    time.sleep(.05)
    print i



#spi.xfer([drive, 10])
#time.sleep(2)
#spi.xfer([drive, 20])
#time.sleep(2)
#spi.xfer([drive, 30])
#time.sleep(2)
#spi.xfer([drive, 50])
#time.sleep(2)




#spi.xfer([drive, 70])
#time.sleep(2)
#spi.xfer([drive, 80])
#time.sleep(2)
#spi.xfer([drive, 90])
#time.sleep(2)
#spi.xfer([drive, 121])
#time.sleep(2)

