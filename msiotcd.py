#!/usr/bin/env python3
# ========================================================================
# msiotcd.py
#
# Description: Daemon to keep msiotc.py running.
#
# Author: Sam Yang, Jim Ing
# Date: 2020-02-21
# ========================================================================

import logging, subprocess, sys, time
from logging.handlers import RotatingFileHandler

import config as cfg

# ------------------------------------------------------------------------
# Initialization
# ------------------------------------------------------------------------

logId = 'msiotcd'
logFile = cfg.logsPath + '/' + logId + '.log'

logging.basicConfig(
    handlers=[RotatingFileHandler(logFile, maxBytes=100000000, backupCount=50)], # 100 MB * 50 = 5 GB
    format='[%(asctime)s.%(msecs)03d] %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------

try:
    # Start the process first time
    logging.info('Started')
    process = subprocess.Popen(['./msiotc.py'])

    while True:
        # Check the state of the process
        status = process.poll()

        if status != None:
            # Terminated, restart process
            process = subprocess.Popen(['./msiotc.py']) # TODO
            logging.info('Termination code: %d' % (status))
            logging.info('Restarted')
        else:
            # Still running
            time.sleep(1)

# Exit cleanly
except KeyboardInterrupt:
    print("\n" + "Stopped")

finally:
    sys.exit(0)
