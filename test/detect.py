#!/usr/bin/env python3
# ========================================================================
# detect.py
#
# Description: 
#
# Author: Jim Ing
# Date: 2020-03-02
# ========================================================================

import subprocess

# Sense HAT
try:
    from sense_hat import SenseHat
    sh = SenseHat()
    hasSensehat = True
except:
    hasSensehat = False
print ('sensehat', hasSensehat)

# Enviro+
try:
    from bme280 import BME280
    bme = BME280()
    hasEnviroplus = True
except:
    hasEnviroplus = False
print ('enviroplus', hasEnviroplus)

# Pi Camera
# https://github.com/raspberrypi-ui/rc_gui/blob/master/src/rc_gui.c#L21
rc = subprocess.check_output('raspi-config nonint get_camera', shell=True)
ret = rc.decode('utf-8').strip() # rc = b'1\n'
if ret == '0':
    hasPiCamera = True
else:
    hasPiCamera = False
print ('picamera', hasPiCamera)

# GPS
try:
    from gps import *
    tmp = gps.gps()
    hasGps = True
except:
    hasGps = False
print ('gps', hasGps)

# I2C (Inter-Integrated-Circuit)
sp = subprocess.check_output("raspi-config nonint get_i2c", shell=True)
rv = sp.decode('utf-8').strip() # rc = b'1\n'
if rv == '0':
    hasI2C = True
else:
    hasI2C = False
print ('i2c', hasI2C)
