import Adafruit_PCA9685
from time import sleep

LOWER_PICKUP = 175
LOWER_DROP = 220
RAISE_SERVO = 400
OPEN_SERVO = 400
CLOSE_SERVO = 260

class claw():

	def __init__(self, liftServoPin, pinchServoPin):

		self.servoControl = Adafruit_PCA9685.PCA9685()

		self.liftServo = liftServoPin
		self.pinchServo = pinchServoPin

		self.resetClaw()

	def __del__(self):
		self.resetClaw()
		self.turnOffClaw()

		del self.servoControl

	def turnOffClaw(self):
		self.servoControl.set_pwm(self.pinchServo, 0, 0)
		self.servoControl.set_pwm(self.liftServo, 0, 0)

	def getPins(self):
		print self.liftServo
		print self.pinchServo
    
	def resetClaw(self):
		
		self.servoControl.set_pwm(self.pinchServo, 0, CLOSE_SERVO)
		sleep(0.25)
		self.servoControl.set_pwm(self.liftServo, 0, RAISE_SERVO)
		sleep(0.25)


	def pickupGift(self):
		print 'picking up'
		
		self.servoControl.set_pwm(self.pinchServo, 0, OPEN_SERVO)
		sleep(1)
		self.servoControl.set_pwm(self.liftServo, 0, LOWER_PICKUP)
		sleep(1)
		self.servoControl.set_pwm(self.pinchServo,0, CLOSE_SERVO)
		sleep(1)
		self.servoControl.set_pwm(self.liftServo, 0, RAISE_SERVO)
		sleep(1)

	def dropGift(self):
		print 'dropping'

		self.servoControl.set_pwm(self.liftServo, 0, LOWER_DROP)
		sleep(1)
		self.servoControl.set_pwm(self.pinchServo, 0, OPEN_SERVO)
		sleep(1)
		self.servoControl.set_pwm(self.liftServo, 0, RAISE_SERVO)
		sleep(1)
		self.servoControl.set_pwm(self.pinchServo, 0, CLOSE_SERVO)
		sleep(1)
