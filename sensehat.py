#!/usr/bin/env python3
# ========================================================================
# sensehat.py
#
# Description: Client for Sense HAT.
#
# Author: Jim Ing
# Date: 2020-01-29
# ========================================================================

import json, logging, random, sys, time

from logging.handlers import RotatingFileHandler
from sense_hat import SenseHat

import config as cfg
import util
from sprites import Sprites

# ------------------------------------------------------------------------
# Initialization
# ------------------------------------------------------------------------

delay_secs = 1

logId = 'sensehat'

logFile = cfg.logsPath + '/' + logId + '.log'
dataFile = cfg.dataPath + '/' + logId + '.json'

dataFileTph = cfg.dataPath + '/data_tph.json'
dataFileAccel = cfg.dataPath + '/data_accelerometer.json'
dataFileGyro = cfg.dataPath + '/data_gyroscope.json'
dataFileCompass = cfg.dataPath + '/data_compass.json'

logging.basicConfig(
    handlers=[RotatingFileHandler(logFile, maxBytes=100000000, backupCount=50)], # 100 MB * 50 = 5 GB
    format='[%(asctime)s.%(msecs)03d] %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

# Do some averaging to decrease jitter
def get_temperature():
    data = {}
    cpu_temp = util.get_cpu_temperature()
    temps = cpu_temps[1:] + [cpu_temp]
    avg_cpu_temp = sum(temps) / float(len(temps))
    raw_temp = sense.get_temperature()
    adj_temp = raw_temp - ((avg_cpu_temp - raw_temp) / cfg.factor)
    data["temperature_cpu"] = cpu_temp
    data["temperature"] = raw_temp
    data["temperature_adj"] = adj_temp

    #data["temperature"] = sense.get_temperature()
    data["temperature_humidity"] = sense.get_temperature_from_humidity()
    data["temperature_pressure"] = sense.get_temperature_from_pressure()
    return data

def get_pressure():
    data = {}
    data["pressure"] = sense.get_pressure()
    return data

def get_humidity():
    data = {}
    data["humidity"] = sense.get_humidity()
    return data

def get_accelerometer():
    data = {}
    sense.set_imu_config(False, False, True) # enable accelerometer only
    data["accelerometer"] = sense.get_accelerometer()
    data["accelerometer_raw"] = sense.get_accelerometer_raw()
    return data

def get_gyroscope():
    data = {}
    sense.set_imu_config(False, True, False) # enable gyroscope only
    gyroscope = sense.get_gyroscope()
    data["gyroscope"] = gyroscope
    data["gyroscopeX"] = gyroscope["pitch"]
    data["gyroscopeY"] = gyroscope["yaw"]
    data["gyroscopeZ"] = gyroscope["roll"]
    data["gyroscope_raw"] = sense.get_gyroscope_raw()
    data["orientation_rad"] = sense.get_orientation_radians()
    data["orientation_deg"] = sense.get_orientation_degrees()
    return data

def get_compass():
    data = {}
    sense.set_imu_config(True, False, False) # enable compass only
    data["compass_north"] = sense.get_compass()
    data["compass_raw"] = sense.get_compass_raw()
    return data

def show_sprite(sid):
    if getattr(sprite, sid):
        sense.clear()
        sense.set_pixels(getattr(sprite, sid))
    return

def show_ghost():
    # Show a random ghost on the LED screen
    pick = random.randint(0, len(sprite.ghosts) - 1)
    if sprite.ghosts[pick]:
        ghost = sprite.ghosts[pick]
        sense.clear()
        sense.set_pixels(ghost)
    return

def show_temperature_line():
    #xn = random.randint(0, 8)
    xn = int(round(iot_data["temperature_adj"])) // 10 # Note: // is the int division operator
    sense.clear()
    for x in range(xn):
        sense.set_pixel(x, 0, 255, 0, 0)
        #sense.set_pixel(x, 1, 255, 0, 0)
        time.sleep(0.05)
    return

def scroll_temperature():
    t = iot_data["temperature_adj"]
    temp = str(round(t, 1)) + 'C'
    if t < 35:
        fg = [0, 255, 0]
    elif t >= 35 and t < 55:
        fg = [255, 255, 0]
    else:
        fg = [255, 0, 0]
    sense.show_message(temp, text_colour=fg)
    return

# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------

sense = SenseHat()
sense.low_light = True
sense.set_rotation(cfg.ledRotation)
sense.clear()

# Temperature
cpu_temps = [util.get_cpu_temperature()] * 5

iot_data = {}
iot_data_tph = {}
iot_data_accel = {}
iot_data_gyro = {}
iot_data_compass = {}

fh = util.open_data_file(dataFile)
fh_tph = util.open_data_file(dataFileTph)
fh_accel = util.open_data_file(dataFileAccel)
fh_gyro = util.open_data_file(dataFileGyro)
fh_compass = util.open_data_file(dataFileCompass)

sprite = Sprites()

try:
    print("Sense HAT: Running (" + cfg.profile + ")\n")
    print("To monitor, use:")
    print("\t" + "$ watch -n 1 cat " + dataFile)
    print("\t" + "$ tail -f " + logFile)

    while True:
        iot_data.update(util.get_current_time())

        iot_data.update(get_temperature())
        iot_data.update(get_pressure())
        iot_data.update(get_humidity())

        iot_data.update(get_accelerometer())
        iot_data.update(get_gyroscope())
        iot_data.update(get_compass())

        iot_data_tph["epoch"] = iot_data["epoch"]
        iot_data_tph["temperature"] = iot_data["temperature"]
        iot_data_tph["pressure"] = iot_data["pressure"]
        iot_data_tph["humidity"] = iot_data["humidity"]

        iot_data_accel["epoch"] = iot_data["epoch"]
        iot_data_accel["accelerometer"] = iot_data["accelerometer"]
        iot_data_accel["accelerometer_raw"] = iot_data["accelerometer_raw"]

        iot_data_gyro["epoch"] = iot_data["epoch"]
        iot_data_gyro["gyroscope"] = iot_data["gyroscope"]
        iot_data_gyro["gyroscopeX"] = iot_data["gyroscopeX"]
        iot_data_gyro["gyroscopeY"] = iot_data["gyroscopeY"]
        iot_data_gyro["gyroscopeZ"] = iot_data["gyroscopeZ"]
        iot_data_gyro["gyroscope_raw"] = iot_data["gyroscope_raw"]
        iot_data_gyro["orientation_rad"] = iot_data["orientation_rad"]
        iot_data_gyro["orientation_deg"] = iot_data["orientation_deg"]

        iot_data_compass["epoch"] = iot_data["epoch"]
        iot_data_compass["compass_north"] = iot_data["compass_north"]
        iot_data_compass["compass_raw"] = iot_data["compass_raw"]

        json_all = json.dumps(iot_data, separators=(',', ':'))
        json_tph = json.dumps(iot_data_tph, separators=(',', ':'))
        json_accel = json.dumps(iot_data_accel, separators=(',', ':'))
        json_gyro = json.dumps(iot_data_gyro, separators=(',', ':'))
        json_compass = json.dumps(iot_data_compass, separators=(',', ':'))
        #print(json_all)

        util.update_data_file(fh, json_all)
        util.update_data_file(fh_tph, json_tph)
        util.update_data_file(fh_accel, json_accel)
        util.update_data_file(fh_gyro, json_gyro)
        util.update_data_file(fh_compass, json_compass)

        logging.info(json_all)

        #show_sprite('smiley')
        show_ghost()
        #show_temperature_line()
        #scroll_temperature()

        time.sleep(delay_secs)

# Exit cleanly
except KeyboardInterrupt:
    print("\n" + "Stopped")

finally:
    sense.clear()
    sys.exit(0)
