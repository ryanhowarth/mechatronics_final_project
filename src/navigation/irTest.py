#!/usr/bin/env python
from Adafruit_ADS1x15 import ADS1x15
from time import sleep

def irDistLeft(volts):
#    return 11.721 * volts**(-0.972)
    return 11.3 * volts**(-0.8959)
#ic=0x00 right
irSensor = ADS1x15(ic=0x00)

while True:
    v = irSensor.readADCSingleEnded(2,4096,250)/1000
    print 'v=',v
    print 'd=',irDistLeft(v)
    sleep(1)
