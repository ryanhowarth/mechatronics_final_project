from Adafruit_ADS1x15 import ADS1x15
from time import sleep

def irDistLeft(volts):
    return 11.721 * volts**(-0.972)

irSensor = ADS1x15(ic=0x00)

while True:
    v0 = irSensor.readADCSingleEnded(0,4096,250)/1000
#    v1 = irSensor.readADCSingleEnded(1,4096,250)/1000
#    v2 = irSensor.readADCSingleEnded(2,4096,250)/1000
    print  v0
    print irDistLeft(v0)
    sleep(.01)
