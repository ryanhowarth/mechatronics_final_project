
from time import sleep
from Adafruit_ADS1x15 import ADS1x15

IR_LEFT = 1
IR_MIDDLE = 2
IR_RIGHT = 3

IR_GAIN = 4096
IR_SPS = 250
i = 0
class irSensor():

	def __init__(self):

		self.sensor = ADS1x15(ic=0x00)
		self.i = 0
	def __del__(self):
		del self.sensor
	#@profile
	def getIrSensorData(self):

		distanceL = []
		distanceM = []
		distanceR = []

		for i in xrange(20):
			voltsL = self.sensor.readADCSingleEnded(IR_LEFT, IR_GAIN, IR_SPS)/1000
			distanceL.append(self.irDistLeft(voltsL))

			voltsM = self.sensor.readADCSingleEnded(IR_MIDDLE, IR_GAIN, IR_SPS)/1000
			distanceM.append(self.irDistMiddle(voltsM))

			voltsR = self.sensor.readADCSingleEnded(IR_RIGHT, IR_GAIN, IR_SPS)/1000
			distanceR.append(self.irDistRight(voltsR))

			sleep(.003)

		finalDistL = sum(distanceL)/len(distanceL)
		finalDistM = sum(distanceM)/len(distanceM)
		finalDistR = sum(distanceR)/len(distanceR)    
	   
		return [finalDistL, finalDistM, finalDistR] 

	def getIrSensorDataNavigation(self):

		distanceL = []
		distanceM = []
		distanceR = []

		for i in xrange(20):
			voltsL = self.sensor.readADCSingleEnded(IR_LEFT, IR_GAIN, IR_SPS)/1000
			distanceL.append(self.irDistLeft(voltsL))

			voltsM = self.sensor.readADCSingleEnded(IR_MIDDLE, IR_GAIN, IR_SPS)/1000
			distanceM.append(self.irDistMiddle(voltsM))

			voltsR = self.sensor.readADCSingleEnded(IR_RIGHT, IR_GAIN, IR_SPS)/1000
			distanceR.append(self.irDistRight(voltsR))

			sleep(.001)

		finalDistL = sum(distanceL)/len(distanceL)
		finalDistM = sum(distanceM)/len(distanceM)
		finalDistR = sum(distanceR)/len(distanceR)    
	   
		return [finalDistL, finalDistM, finalDistR] 



	def irDistLeft(self, volts):
	#	return 10.189 * volts**(-0.969)
		return 11.3 * volts**(-0.9558)

	def irDistMiddle(self, volts):
	#	return 11.714 * volts**(-1.038)
		return 11.3 * volts**(-0.8959)

	def irDistRight(self, volts):
	#	return 9.6902 * volts**(-0.954)
		return 11.65 * volts**(-1.048)


