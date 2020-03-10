#!/usr/bin/env python3
# ========================================================================
# cmds.py
#
# Description: Commands for remote execution from IoT Central dashboard.
#
# Author: Jim Ing
# Date: 2020-02-09
# ========================================================================

import RPi.GPIO as GPIO
import subprocess

def toggle_relay(gpio_pin):
    pin_num = int(gpio_pin) # channel must be an integer
    #print("toggle_relay", pin_num)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_num, GPIO.OUT)

    state = GPIO.input(pin_num)

    if state:
        GPIO.output(pin_num, False)
    else:
        GPIO.output(pin_num, True)

    state = GPIO.input(pin_num)
    return state

def take_photo():
    sp = subprocess.check_output('./camera.py')
    rv = sp.decode('utf-8').strip() # sp = b'1\n'
    return rv
