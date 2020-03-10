#!/usr/bin/env python3
# ========================================================================
# camera.py
#
# $ crontab -e
# 0,15,30,45 * * * * python /home/pi/Projects/camera.py > /home/pi/Projects/camera.log 2>&1
# ========================================================================

try:
    import base64
    from picamera import PiCamera, Color
    from time import sleep
    from datetime import datetime

    #import config as cfg

    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    timestamp_file = now.strftime('%Y%m%d-%H%M%S')
    #screencap = '/home/pi/Pictures/' + timestamp_file + '.jpg'
    screencap = './snapshot/' + timestamp_file + '.jpg'

    camera = PiCamera()
    camera.rotation = 0
    camera.resolution = (800, 600)
    camera.framerate = 15
    camera.exposure_mode = 'auto'
    camera.annotate_background = Color('black')
    camera.annotate_foreground = Color('white')
    camera.annotate_text_size = 10
    camera.annotate_text = timestamp

    #camera.start_preview(alpha=200)
    #sleep(3)
    camera.capture(screencap)
    #camera.stop_preview()
    camera.close()

    with open(screencap, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
    #print(my_string)
    #print(my_string.decode('utf-8'))
    #print(len(my_string))
    print(screencap)

except:
    print("\n" + "Camera error")
