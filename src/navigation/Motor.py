import wiringpi as wp

wp.wiringPiSetupGpio()

INPUT_MODE = 0
OUTPUT_MODE = 1
PWM_MODE = 2

PWM_MIN = 0
PWM_MAX = 1024

HIGH = 1
LOW = 0

class motor():

	def __init__(self, outputPinA, outputPinB, pwmPin):

		self.outA = outputPinA
		self.outB = outputPinB
		wp.pinMode(self.outA, OUTPUT_MODE)
		wp.pinMode(self.outB, OUTPUT_MODE)
		self.forward()

		wp.pwmSetMode(0)
		wp.pwmSetClock(400)
		wp.pwmSetRange(PWM_MAX)

		self.pwm = pwmPin
		wp.pinMode(self.pwm, PWM_MODE)
		self.setSpeed(PWM_MIN)

	def __del__(self):
		
		wp.pwmWrite(self.pwm, PWM_MIN)
		wp.digitalWrite(self.outA, LOW)
		wp.digitalWrite(self.outB, LOW)

		wp.pinMode(self.pwm, INPUT_MODE)
		wp.pinMode(self.outA, INPUT_MODE)
		wp.pinMode(self.outB, INPUT_MODE)

	def forward(self):
		wp.digitalWrite(self.outA, LOW)
		wp.digitalWrite(self.outB, HIGH)
	
	def backward(self):
		
		wp.digitalWrite(self.outA, HIGH)
		wp.digitalWrite(self.outB, LOW)

	def setSpeed(self, speed):

		# Constrain 
		if speed > PWM_MAX:
			speed = PWM_MAX
		elif speed < PWM_MIN:
			speed = PWM_MIN

		wp.pwmWrite(self.pwm, speed)

	def getPins(self):
		print self.outA
		print self.outB
		print self.pwm

	def stop(self):
		wp.pwmWrite(self.pwm, PWM_MIN)
