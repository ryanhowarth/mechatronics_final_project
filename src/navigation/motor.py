import wiringpi as wp



INPUT_MODE = 0
OUTPUT_MODE = 1
PWM_MODE = 2

PWM_MIN = 0
PWM_MAX = 1024

HIGH = 1
LOW = 0

class motor():

	outA = 0
	outB = 0
	pwm = 0

	def __init__(self, outputPinA, outputPinB, pwmPin):

		outA = outputPinA
		outB = outputPinB
		wp.pinMode(outA, OUTPUT_MODE)
		wp.pinMode(outB, OUTPUT_MODE)
		self.forward()

		wp.pwmSetMode(0)
		wp.pwmSetClock(400)
		wp.pwmSetRange(PWM_MAX)

		pwm = pwmPin
		wp.pinMode(pwm, PWM_MODE)
		self.setSpeed(PWM_MIN)

	def __del__(self):
		wp.digitalWrite(self.outA, LOW)
		wp.digitalWrite(self.outB, LOW)
		wp.pwmWrite(self.pwm, PWM_MIN)

		wp.pinMode(self.outA, INPUT_MODE)
		wp.pinMode(self.outB, INPUT_MODE)
		wp.pinMode(self.pwm, INPUT_MODE)

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

	def stop(self):
		wp.pwmWrite(self.pwm, PWM_MIN)
