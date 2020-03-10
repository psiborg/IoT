# IoT

This is a repo for exploring IoT (Internet of Things) using Single Board Computers (SBC).

![Pi-based IoT Architecture](docs/overview.png?display=True "Pi-based IoT Architecture")

## 1. Requirements

* Raspberry Pi 3 Model B+ **&ndash;or&ndash;** Pi Zero WH
* Enviro+ pHAT **&ndash;or&ndash;** Sense HAT
* U-blox7 GPS/GLONASS &mdash; *(optional)*
* Sabre Water Leak Alarm &mdash; *(optional)*
* Raspian (Buster)
* Python 3.7

## 2. Setup

### 2a. Local

* cd IoT
* mkdir data
* mkdir logs
* chmod 755 *.py

### 2b. Base (for Raspian Lite)

* sudo apt-get install git

* pip install spidev
* pip3 install spidev

* pip install RPi.GPIO
* pip3 install RPi.GPIO

### 2c. Azure IoT Central

* pip install iotc
* pip3 install iotc

### 2d. Enviro+ pHAT

* curl -sSL https://get.pimoroni.com/enviroplus | bash

### 2e. Sense HAT

* pip install sense_hat

### 2f. U-blox7

* sudo apt-get install gpsd gpsd-clients python-gps
* pip install gps
* pip3 install gps

  *Testing:*

  * cgps -s
  * gpsmon

## 3. Configuring

* cd IoT
* nano config.py

## 4. Running

* cd IoT
* ./enviro.py **&ndash;or&ndash;** ./sensehat.py &mdash; **(required)**
* ./ublox7.py &mdash; *(optional)*
* ./msiotcd.py &mdash; **(required)**

## 5. Monitoring

* cd IoT/data/logs
* tail -f msiotc.log

## 6. Reference

- [Use gpsd](https://learn.adafruit.com/adafruit-ultimate-gps-hat-for-raspberry-pi/use-gpsd)
- [gpsd_json — gpsd request/response protocol](https://gpsd.gitlab.io/gpsd/gpsd_json.html)
- [Connect a Raspberry Pi to your Azure IoT Central application (Python)](https://docs.microsoft.com/en-us/azure/iot-central/core/howto-connect-raspberry-pi-python)
- [iotc - Azure IoT Central - Python (light) device SDK Documentation](https://pypi.org/project/iotc/)
- [enviroplus-python](https://github.com/pimoroni/enviroplus-python)
- [Sense HAT Python Module](https://pythonhosted.org/sense-hat/)
- [picamera](https://picamera.readthedocs.io/en/release-1.10/index.html)
- [raspi-config nonint](https://github.com/raspberrypi-ui/rc_gui/blob/master/src/rc_gui.c#L21)
