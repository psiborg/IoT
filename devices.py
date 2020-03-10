#!/usr/bin/env python3
# ========================================================================
# config.py
#
# Description: Device checker.
#
# Author: Jim Ing
# Date: 2020-02-24
# ========================================================================

import subprocess

# ------------------------------------------------------------------------
# Pi Camera
# ------------------------------------------------------------------------

sp = subprocess.check_output("raspi-config nonint get_camera", shell=True)
rv = sp.decode('utf-8').strip() # sp = b'1\n'
if rv == '0':
    hasPiCamera = True
else:
    hasPiCamera = False

# ------------------------------------------------------------------------
# Enviro+
# ------------------------------------------------------------------------

try:
    from bme280 import BME280
    bme = BME280()
    hasEnviroplus = True
except:
    hasEnviroplus = False

# ------------------------------------------------------------------------
# Sense HAT
# ------------------------------------------------------------------------

try:
    from sense_hat import SenseHat
    sh = SenseHat()
    hasSensehat = True
except:
    hasSensehat = False

# ------------------------------------------------------------------------
# GPS
# ------------------------------------------------------------------------

try:
    # TODO:
    from gps import *
    tmp = gps.gps()
    hasGps = True
except:
    hasGps = False
