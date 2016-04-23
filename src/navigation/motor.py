import wiringpi as wp

class motor()

	INPUT_MODE = 0
	OUTPUT_MODE = 1
	PWM_MODE = 2

	PWM_MIN = 0
	PWM_MAX = 1024

	HIGH = 1
	LOW = 0

	outA = 0
	outB = 0
	pwm = 0

	def __init__(self, outputPinA, outputPinB, pwmPin):

		outA = outputPinA
		outB = outputPinB
		wp.pinMode(outA, OUTPUT_MODE)
		wp.pinMode(outB, OUTPUT_MODE)
		forward()

		wp.pwmSetMode(0)
		wp.pwmSetClock(400)
		wp.pwmSetRange(PWM_MAX)

		pwm = pwmPin
		wp.pinMode(pwm, PWM_MODE)
		setSpeed(PWM_MIN)

	def __del__(self):
		wp.digitalWrite(outA, LOW)
		wp.digitalWrite(outB, LOW)
		wp.pwmWrite(pwm, PWM_MIN)

		wp.pinMode(outA, INPUT_MODE)
		wp.pinMode(outB, INPUT_MODE)
		wp.pinMode(pwm, INPUT_MODE)

	def forward(self):
		wp.digitalWrite(inA, LOW)
		wp.digitalWrite(inB, HIGH)

	def backward(self):
		wp.digitalWrite(inA, HIGH)
		wp.digitalWrite(inB, LOW)

	def setSpeed(self, speed):

		# Constrain 
		if speed > PWM_MAX:
			speed = PWM_MAX
		elif speed < PWM_MIN:
			speed = PWM_MIN

		wp.pwmWrite(pwm, speed)

	def stop(self):
		wp.pwmWrite(pwm, PWM_MIN)