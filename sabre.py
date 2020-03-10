#!/usr/bin/env python3
# ========================================================================
# sabre.py
#
# Description: Client for Sabre Water Leak Alarm.
#
# Author: Sam Yang, Jim Ing
# Date: 2020-03-06
# ========================================================================

import json, logging, sys, time
import RPi.GPIO as GPIO
from logging.handlers import RotatingFileHandler

import config as cfg
import util

# ------------------------------------------------------------------------
# Initialization
# ------------------------------------------------------------------------

delay_secs = 5

logId = 'sabre'

logFile = cfg.logsPath + '/' + logId + '.log'
dataFile = cfg.dataPath + '/' + logId + '.json'
dataFileWater = cfg.dataPath + '/data_water.json'

logging.basicConfig(
    handlers=[RotatingFileHandler(logFile, maxBytes=100000000, backupCount=50)], # 100 MB * 50 = 5 GB
    format='[%(asctime)s.%(msecs)03d] %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

def get_water(gpio_pin):
    pin_num = int(gpio_pin)
    data = {}
    state = GPIO.input(pin_num)
    if state == False:
        data["detected"] = True
    else:
        data["detected"] = False
    return data

# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------

iot_data = {}
iot_data_water = {}

fh = util.open_data_file(dataFile)
fh_water = util.open_data_file(dataFileWater)

try:
    print("Sabre Water Leak Alarm: Running (" + cfg.profile + ") on pin " + str(cfg.gpioPinWaterLeakAlarm) + "\n")
    print("To monitor, use:")
    print("\t" + "$ watch -n 1 cat " + dataFile)
    print("\t" + "$ tail -f " + logFile)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(cfg.gpioPinWaterLeakAlarm, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while True:
        iot_data.update(util.get_current_time())

        iot_data.update(get_water(cfg.gpioPinWaterLeakAlarm))

        iot_data_water["epoch"] = iot_data["epoch"]
        iot_data_water["detected"] = iot_data["detected"]

        json_all = json.dumps(iot_data, separators=(',', ':'))
        json_water = json.dumps(iot_data_water, separators=(',', ':'))
        logging.info(json_all)
        #print(json_all)

        util.update_data_file(fh, json_all)
        util.update_data_file(fh_water, json_water)

        time.sleep(delay_secs)

# Exit cleanly
except KeyboardInterrupt:
    print("\n" + "Stopped")

finally:
    GPIO.cleanup()
    sys.exit(0)
