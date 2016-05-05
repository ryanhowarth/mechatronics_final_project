import threading
import time
import IrSensor

TIME_TO_SLEEP = 0.001
class irSensorController(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.timeToSleep = TIME_TO_SLEEP
		self.running = False
		self.irSensors = IrSensor.irSensor()
		
	def run(self):
		self.running = True
		while(self.running):
			#update ir sensor data
			self.getIrSensorData()
			#sleep
			time.sleep(self.timeToSleep)
		self.running = False
	def stopController(self):
		self.running = False
	def getIrSensorData(self):
		return self.irSensors.getIrSensorData()
	
