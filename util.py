#!/usr/bin/env python3
# ========================================================================
# util.py
#
# Description: Utility functions.
#
# Author: Jim Ing
# Date: 2020-01-29
# ========================================================================

import os.path
import time
from datetime import datetime
from subprocess import PIPE, Popen

def open_data_file(filePath):
    fh_exists = os.path.isfile(filePath)
    if fh_exists:
        fh = open(filePath, "r+")
    else:
        fh = open(filePath, "w")
    return fh

# Use seek and truncate to avoid race conditions from opening and closing the file
def update_data_file(fh, str):
    fh.seek(0)
    fh.write(str)
    fh.truncate()
    return

def get_current_time():
    cur = time.time()
    data = {}
    data["epoch"] = cur
    data["datetime_local"] = datetime.fromtimestamp(cur).strftime('%Y-%m-%d %H:%M:%S')
    data["datetime_utc"] = datetime.utcfromtimestamp(cur).strftime('%Y-%m-%d %H:%M:%S')
    return data

# Get the temperature of the CPU
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])
