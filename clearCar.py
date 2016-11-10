#!/usr/bin/env python
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import spidev
import time

drive = 16
angle = 0
spi = spidev.SpiDev()
spi.open(0,0)
spi.xfer([drive,118])
time.sleep(1)
spi.xfer([angle,128])
spi.xfer([drive,128])
