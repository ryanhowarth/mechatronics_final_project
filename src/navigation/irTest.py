from Adafruit_ADS1x15 import ADS1x15
from time import sleep

def irDistLeft(volts):
    return 11.721 * volts**(-0.972)

irSensor = ADS1x15(ic=0x00)

while True:
    v = irSensor.readADCSingleEnded(1,4096,250)/1000
    print v
    print irDistLeft(v)
    sleep(1)
