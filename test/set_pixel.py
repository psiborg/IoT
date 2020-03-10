#!/usr/bin/env python3

import random, sys, time
from sense_hat import SenseHat

try:
    sense = SenseHat()
    sense.clear()

    # examples using (x, y, r, g, b)
    sense.set_pixel(0, 0, 255, 0, 0)
    sense.set_pixel(0, 7, 0, 255, 0)
    sense.set_pixel(7, 0, 0, 0, 255)
    sense.set_pixel(7, 7, 255, 0, 255)

    while True:
        sense.clear()

        r = random.randint(0, 8)
        g = random.randint(0, 8)
        b = random.randint(0, 8)
        
        for x1 in range(r):
            sense.set_pixel(x1, 0, 255, 0, 0)
            #sense.set_pixel(x1, 1, 255, 0, 0)
            #time.sleep(0.05)

        for x2 in range(g):
            sense.set_pixel(x2, 3, 0, 255, 0)
            #sense.set_pixel(x2, 4, 0, 255, 0)
            #time.sleep(0.05)

        for x3 in range(b):
            sense.set_pixel(x3, 6, 0, 0, 255)
            #sense.set_pixel(x3, 7, 0, 0, 255)
            #time.sleep(0.05)

        time.sleep(0.15)

# Exit cleanly
except KeyboardInterrupt:
    print("\n" + "Stopped")
    sense.clear()
    sys.exit(0)
