#!/usr/bin/env python3

import io, iotc, json, logging, time
from iotc import IOTConnectType, IOTLogLevel
from datetime import datetime
from random import randint

import config as cfg

mslog = logging.getLogger('msiotc_test')
msfh = logging.FileHandler('msiotc_test.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
msfh.setFormatter(formatter)
mslog.addHandler(msfh)
mslog.setLevel(logging.DEBUG)

iotc = iotc.Device(cfg.scopeId, cfg.deviceKey, cfg.deviceId, IOTConnectType.IOTC_CONNECT_SYMM_KEY)
iotc.setLogLevel(IOTLogLevel.IOTC_LOGGING_API_ONLY)

mslog.info('Profile: ' + str(cfg.profile))

gCanSend = False
gCounter = 0

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
        #iotc.disconnect()
        #print("Waiting to reconnect...")
        #time.sleep(30)
        #print("Trying to reconnect...")
        #iotc.connect()

def onmessagesent(info):
    #print("\t- [onmessagesent] => " + str(info.getPayload()))
    mslog.info('[onmessagesent] => ' + str(info.getPayload()))

def oncommand(info):
    #print("- [oncommand] => " + info.getTag() + " => " + str(info.getPayload()))
    mslog.info('[oncommand] => ' + info.getTag() + ' => ' +  + str(info.getPayload()))

def onsettingsupdated(info):
    #print("- [onsettingsupdated] => " + info.getTag() + " => " + info.getPayload())
    mslog.info('[onsettingsupdated] => ' + info.getTag() + ' => ' + info.getPayload())

iotc.on("ConnectionStatus", onconnect)
iotc.on("MessageSent", onmessagesent)
iotc.on("Command", oncommand)
iotc.on("SettingsUpdated", onsettingsupdated)

iotc.connect()

while iotc.isConnected():
    iotc.doNext()
    if gCanSend == True:
        if gCounter % 20 == 0:
            gCounter = 0
            cur = time.time()
            now = datetime.utcfromtimestamp(cur).strftime('%Y-%m-%d %H:%M:%S')
            jsonStr = '{"temperature": ' + str(randint(20, 45)) + '}'
            print("[" + now + "] Sending telemetry...", gCounter)
            iotc.sendTelemetry(jsonStr)

        gCounter += 1
