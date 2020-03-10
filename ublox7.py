#!/usr/bin/env python3
# ========================================================================
# ublox7.py
#
# Description: Client for U-blox7 GPS/GLONASS USB adapter.
#
# Author: Jim Ing
# Date: 2020-01-30
# ========================================================================

import json, logging, sys, time
from logging.handlers import RotatingFileHandler
from requests import get
from gps import *

import config as cfg
import util

# ------------------------------------------------------------------------
# Initialization
# ------------------------------------------------------------------------

delay_secs = 1

logId = 'ublox7'

logFile = cfg.logsPath + '/' + logId + '.log'
dataFile = cfg.dataPath + '/' + logId + '.json'
dataFileGps = cfg.dataPath + '/data_gps.json'

logging.basicConfig(
    handlers=[RotatingFileHandler(logFile, maxBytes=100000000, backupCount=50)], # 100 MB * 50 = 5 GB
    format='[%(asctime)s.%(msecs)03d] %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

#ip_addr = "99.246.59.59" # Rogers
#ip_addr = "69.158.246.169" # Bell
ip_addr = "38.99.130.114"
#ip_data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
#ip_addr = ip_data["ip"]

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

def get_geo():
    resp = get('https://geo.ipify.org/api/v1?apiKey=' + cfg.ipify['api_key'] + '&ipAddress=' + ip_addr).text
    json_obj = json.loads(resp)
    json_str = json.dumps(json_obj, indent=2, sort_keys=True)
    #print(json_str)
    #print(json_obj["location"]["lat"], json_obj["location"]["lng"])

    data = {}
    data["assetloc"] = {}
    data["assetloc"]["lat"] = json_obj["location"]["lat"]
    data["assetloc"]["lon"] = json_obj["location"]["lng"]
    #print(data)

    return data

# https://gpsd.gitlab.io/gpsd/gpsd_json.html
def get_gps():
    try:
        data = {}
        report = gpsd.next()
        #print(report['class'])

        if report['class'] == 'TPV': # TPV (Time Position Velocity)
            # Get data
            lat = getattr(report, 'lat', '')
            lon = getattr(report, 'lon', '')
            tm = getattr(report, 'time', '') # ISO8601 format
            alt = getattr(report, 'alt', '')
            speed = getattr(report, 'speed', '') # Speed over ground, meters per second
            epx = getattr(report, 'epx', '') # Longitude error estimate in meters
            epy = getattr(report, 'epy', '') # Latitude error estimate in meters
            data["assetloc"] = {}
            data["assetloc"]["lat"] = lat
            data["assetloc"]["lon"] = lon
            data["assetloc"]["alt"] = alt
            data["assetloc"]["epx"] = epx
            data["assetloc"]["epy"] = epy
            logging.info('TPV: ' + json.dumps(data))
        elif report['class'] == 'VERSION':
            logging.debug('VERSION: release=' + report['release'])
        elif report['class'] == 'DEVICES':
            if report['devices'] and report['devices'][0]:
                logging.debug('DEVICES: driver=' + report['devices'][0]['driver'])
        elif report['class'] == 'WATCH':
            logging.debug('WATCH: enable=' + str(report['enable']))
        elif report['class'] == 'SKY':
            logging.debug('SKY: satellites=' + str(len(report['satellites'])))
        else:
            logging.debug(report['class'])

    except:
        err = sys.exc_info()[0]
        logging.error(err)

    return data

# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------

iot_data = {}
iot_data_gps = {}

fh = util.open_data_file(dataFile)
fh_gps = util.open_data_file(dataFileGps)

try:
    print("U-blox7 GPS/GLONASS: Running (" + cfg.profile + ")\n")
    print("To monitor, use:")
    print("\t" + "$ watch -n 1 cat " + dataFile)
    print("\t" + "$ tail -f " + logFile)

    # Use IP geolocation as a fallback
    geo_data = get_geo()
    iot_data.update(geo_data)
    iot_data["geo"] = iot_data["assetloc"]
    iot_data_gps["assetloc"] = iot_data["assetloc"]

    json_all = json.dumps(iot_data, separators=(',', ':'))
    logging.info(json_all)

    gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)

    while True:
        iot_data.update(util.get_current_time())
        iot_data_gps["epoch"] = iot_data["epoch"]

        gps_data = get_gps()

        if "assetloc" in gps_data and "lat" in gps_data["assetloc"]:
            if gps_data["assetloc"]["lat"] != '' and gps_data["assetloc"]["lon"] != '':
                iot_data.update(gps_data)
                iot_data_gps["assetloc"] = iot_data["assetloc"]

        json_all = json.dumps(iot_data, separators=(',', ':'))
        json_gps = json.dumps(iot_data_gps, separators=(',', ':'))
        #print(json_all)

        util.update_data_file(fh, json_all)
        util.update_data_file(fh_gps, json_gps)

        if "assetloc" in gps_data:
            if "lat" in gps_data["assetloc"]:
                logging.info(json_all)

        time.sleep(delay_secs)

# Exit cleanly
except KeyboardInterrupt:
    print("\n" + "Stopped")

finally:
    sys.exit(0)
