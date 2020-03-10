#!/usr/bin/env python3
# ========================================================================
# enviro.py
#
# Description: Client for Pimoroni Enviro+ pHAT.
#
# Author: Jim Ing
# Date: 2020-01-29
# ========================================================================

import json, logging, sys, time

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

import ST7735

from bme280 import BME280
from enviroplus import gas
from PIL import Image, ImageDraw, ImageFont

from logging.handlers import RotatingFileHandler

import config as cfg
import devices as dev
import util
import cmds

# ------------------------------------------------------------------------
# Initialization
# ------------------------------------------------------------------------

delay_secs = 1

logId = 'enviro'

logFile = cfg.logsPath + '/' + logId + '.log'
dataFile = cfg.dataPath + '/' + logId + '.json'

dataFileTph = cfg.dataPath + '/data_tph.json'
dataFileLight = cfg.dataPath + '/data_light.json'
dataFileGas = cfg.dataPath + '/data_gas.json'

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
    raw_temp = tph.get_temperature()
    adj_temp = raw_temp - ((avg_cpu_temp - raw_temp) / cfg.factor)
    data["temperature_cpu"] = cpu_temp
    data["temperature"] = raw_temp
    data["temperature_adj"] = adj_temp
    return data

def get_pressure():
    data = {}
    data["pressure"] = tph.get_pressure()
    return data

def get_humidity():
    data = {}
    data["humidity"] = tph.get_humidity()
    return data

def get_lux():
    data = {}
    data["light"] = ltr559.get_lux()
    return data

def get_proximity():
    data = {}
    data["proximity"] = ltr559.get_proximity()
    return data

def get_gases():
    gas_data = gas.read_all()
    data = {}
    data["gas"] = {}
    data["gas"]["ammonia"] = gas_data.nh3 / 1000
    data["gas"]["carbon_monoxide"] = gas_data.reducing / 1000
    data["gas"]["nitrogen_dioxide"] = gas_data.oxidising / 1000
    return data

def display_readings():
    draw.rectangle((0, 0, 160, 80), bg_color)

    draw.text((0, 0), iot_data['datetime_local'], font=smallfont, fill=fg_color)

    draw.text((0, 16), 'Temp: ' + str(round(iot_data['temperature_adj'], 1)) + '°C', font=smallfont, fill=fg_color)
    draw.text((0, 30), 'Pres: ' + str(round(iot_data['pressure'], 0)) + ' hPa', font=smallfont, fill=fg_color)
    draw.text((0, 44), 'Humi: ' + str(round(iot_data['humidity'], 0)) + '%', font=smallfont, fill=fg_color)
    draw.text((0, 60), 'Lux: ' + str(round(iot_data['light'], 0)) + '', font=smallfont, fill=fg_color)

    draw.text((90, 16), 'NH3: ' + str(round(iot_data['gas']['ammonia'], 0)) + ' kO', font=smallfont, fill=fg_color)
    draw.text((90, 30), 'CO: ' + str(round(iot_data['gas']['carbon_monoxide'], 0)) + ' kO', font=smallfont, fill=fg_color)
    draw.text((90, 44), 'NO2: ' + str(round(iot_data['gas']['nitrogen_dioxide'], 0)) + ' kO', font=smallfont, fill=fg_color)
    draw.text((90, 60), 'Prox: ' + str(round(iot_data['proximity'], 0)) + '', font=smallfont, fill=fg_color)

    disp.display(img)
    return

def check_proximity():
    if dev.hasPiCamera == True:
        if iot_data['proximity'] > cfg.proximityTrigger:
            resp = cmds.take_photo()
            logging.info('Took photo ' + str(resp))
    return

# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------

# Create LCD class instance
disp = ST7735.ST7735(
    port = 0,
    cs = 1,
    dc = 9,
    backlight = 12,
    rotation = 270,
    spi_speed_hz = 10000000
)

# Initialize display
disp.begin()

# Width and height to calculate text position
w = disp.width
h = disp.height

# New canvas to draw on
img = Image.new('RGB', (w, h), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

# Text settings
#fontFamily = "fonts/Asap/Asap-Regular.ttf"
fontFamily = "fonts/calibri.ttf"
#fontFamily = "fonts/segoeui.ttf"
font = ImageFont.truetype(fontFamily, 22)
smallfont = ImageFont.truetype(fontFamily, 12)
fg_color = (255, 255, 255)
bg_color = (0, 0, 0)

# Temperature
cpu_temps = [util.get_cpu_temperature()] * 5
tph = BME280()

iot_data = {}
iot_data_tph = {}
iot_data_light = {}
iot_data_gas = {}

fh = util.open_data_file(dataFile)
fh_tph = util.open_data_file(dataFileTph)
fh_light = util.open_data_file(dataFileLight)
fh_gas = util.open_data_file(dataFileGas)

try:
    print("Enviro+ pHAT: Running (" + cfg.profile + ")\n")
    print("To monitor, use:")
    print("\t" + "$ watch -n 1 cat " + dataFile)
    print("\t" + "$ tail -f " + logFile)

    while True:
        iot_data.update(util.get_current_time())

        iot_data.update(get_temperature())
        iot_data.update(get_pressure())
        iot_data.update(get_humidity())
        iot_data.update(get_lux())
        iot_data.update(get_proximity())
        iot_data.update(get_gases())

        iot_data_tph["epoch"] = iot_data["epoch"]
        iot_data_tph["temperature"] = iot_data["temperature"]
        iot_data_tph["pressure"] = iot_data["pressure"]
        iot_data_tph["humidity"] = iot_data["humidity"]

        iot_data_light["epoch"] = iot_data["epoch"]
        iot_data_light["light"] = iot_data["light"]
        iot_data_light["proximity"] = iot_data["proximity"]

        iot_data_gas["epoch"] = iot_data["epoch"]
        iot_data_gas["gas"] = iot_data["gas"]

        json_all = json.dumps(iot_data, separators=(',', ':'))
        json_tph = json.dumps(iot_data_tph, separators=(',', ':'))
        json_light = json.dumps(iot_data_light, separators=(',', ':'))
        json_gas = json.dumps(iot_data_gas, separators=(',', ':'))
        #print(json_all)

        util.update_data_file(fh, json_all)
        util.update_data_file(fh_tph, json_tph)
        util.update_data_file(fh_light, json_light)
        util.update_data_file(fh_gas, json_gas)

        logging.info(json_all)

        display_readings()
        check_proximity()

        time.sleep(delay_secs)

# Exit cleanly
except KeyboardInterrupt:
    print("\n" + "Stopped")

finally:
    disp.set_backlight(0)
    sys.exit(0)
