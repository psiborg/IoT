#!/usr/bin/env python3
# ========================================================================
# msiotc.py
#
# Description: Client for Microsoft IoT Central.
#
# Author: Jim Ing
# Date: 2020-01-29
# ========================================================================

import io, iotc, json, logging, os, sys, time
from iotc import IOTConnectType, IOTLogLevel
from datetime import datetime
#from random import randint

import config as cfg
import devices as dev
import util
import cmds

# ------------------------------------------------------------------------
# Initialization
# ------------------------------------------------------------------------

logId = 'msiotc'
logFile = cfg.logsPath + '/' + logId + '.log'

mslog = logging.getLogger(logId)
msfh = logging.FileHandler(logFile)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
msfh.setFormatter(formatter)
mslog.addHandler(msfh)
mslog.setLevel(logging.DEBUG)

iotc = iotc.Device(cfg.scopeId, cfg.deviceKey, cfg.deviceId, IOTConnectType.IOTC_CONNECT_SYMM_KEY)
iotc.setLogLevel(IOTLogLevel.IOTC_LOGGING_API_ONLY)
iotc.setTokenExpiration(cfg.tokenExpiry * 24 * 3600) # in seconds

#print('Profile:', cfg.profile)
mslog.info('Profile: ' + str(cfg.profile))

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

def show_pixel(style):
    if dev.hasSensehat == True:
        if style == 'send':
            dev.sh.set_pixel(0, 0, 255, 0, 0) # (x, y, r, g, b)
        elif style == 'recv':
            dev.sh.set_pixel(0, 0, 0, 255, 0)
        else:
            dev.sh.set_pixel(0, 0, 0, 0, 0)
    # TODO:
    #elif dev.hasEnviroplus == True:
        #print("Show something")
    return

def onconnect(info):
    global gCanSend
    #print("- [onconnect] => status:" + str(info.getStatusCode()))
    mslog.info('[onconnect] => status: ' + str(info.getStatusCode()))
    if info.getStatusCode() == 0:
        if iotc.isConnected():
            mslog.info('Connected')
            gCanSend = True
        else:
            mslog.info('Not connected?')
    else:
        print('Disconnected due to status code (' + str(info.getStatusCode()) + ')')
        mslog.error('Disconnected due to status code (' + str(info.getStatusCode()) + ')')

def onmessagesent(info):
    #print("\t- [onmessagesent] => " + str(info.getPayload()))
    mslog.info('[onmessagesent] => ' + str(info.getPayload()))
    show_pixel('recv')

def oncommand(info):
    #print("- [oncommand] => " + info.getTag() + " => " + str(info.getPayload()))
    mslog.info('[oncommand] => ' + info.getTag() + ' => ' + str(info.getPayload()))
    if cfg.hasRelay == True:
        resp = cmds.toggle_relay(cfg.gpioPin)
        mslog.info('Toggled relay on pin ' + str(cfg.gpioPin) + ' to ' + str(resp))
    elif dev.hasPiCamera == True:
        resp = cmds.take_photo()
        mslog.info('Took photo ' + str(resp))
    else:
        print("Received remote command")

def onsettingsupdated(info):
    #print("- [onsettingsupdated] => " + info.getTag() + " => " + info.getPayload())
    mslog.info('[onsettingsupdated] => ' + info.getTag() + ' => ' + info.getPayload())

# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------

try:
    print("Azure IoT Central Client: Running (" + cfg.profile + ")\n")
    print("To monitor, use:")
    print("\t" + "$ tail -f " + logFile)

    iotc.on("ConnectionStatus", onconnect)
    iotc.on("MessageSent", onmessagesent)
    iotc.on("Command", oncommand)
    iotc.on("SettingsUpdated", onsettingsupdated)

    filePath = ''
    iotData = {}

    gCanSend = False
    gCounter = 0

    iotc.connect()

    while iotc.isConnected():
        iotc.doNext()
        if gCanSend == True:
            if gCounter % cfg.gInterval == 0:
                show_pixel('clear')
                gCounter = 0
                cur = time.time()
                now = datetime.utcfromtimestamp(cur).strftime('%Y-%m-%d %H:%M:%S')

                for filename in os.listdir(cfg.dataPath):
                    if filename.startswith("data_") and filename.endswith(".json"):
                        filePath = os.path.join(cfg.dataPath, filename)
                        #print(filePath)
                        with open(filePath, 'r') as json_file:
                            try:
                                json_obj = json.load(json_file)
                                #iotData.update(json_obj)
                                diff = int(cur) - int(json_obj['epoch'])
                                if diff < cfg.secsTooOld:
                                    iotData.update(json_obj)
                                else:
                                    mslog.warning("Skipping " + filePath + " because it is too old [" + str(diff) + " secs]")
                            except ValueError as err:
                                mslog.error(err)
                                mslog.error(json_file)

                iotData['epoch'] = cur
                #print(iotData)

                #jsonStr = '{"temperature": ' + str(randint(20, 45)) + '}'
                jsonStr = json.dumps(iotData)
                #print(jsonStr)
                #print("[" + now + "] Sending telemetry...", gCounter)
                show_pixel('send')
                iotc.sendTelemetry(jsonStr)

            gCounter += 1

# Exit cleanly
except KeyboardInterrupt:
    print("\n" + "Stopped")

finally:
    if dev.hasSensehat == True:
        dev.sh.clear()
    sys.exit(0)
