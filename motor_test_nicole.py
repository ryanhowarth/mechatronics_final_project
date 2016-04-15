import wiringpi as wp
from time import sleep

PWM0 = 18 #pin12
PWM1 = 13 #pin33
PIN1 = 25 #pin22
PIN2 = 8 #pin24
PIN3 = 9 #pin21
PIN4 = 11 #pin23
 
PWM_MODE = 2
ON = 1
OFF = 0

wp.wiringPiSetupGpio()

#enable PWM0
wp.pinMode(PWM0, PWM_MODE)  #set pin to pwm mode
wp.pwmWrite(PWM0, OFF)

#enable PWM1
wp.pinMode(PWM1, PWM_MODE)
wp.pwmWrite(PWM1, OFF)

#enable pins motor1
wp.pinMode(PIN1, 1)
wp.pinMode(PIN2, 1)
wp.digitalWrite(PIN1, ON)
wp.digitalWrite(PIN2, OFF)

wp.pinMode(PIN3,1)
wp.pinMode(PIN4,1)
wp.digitalWrite(PIN3, ON)
wp.digitalWrite(PIN4, OFF)

try:

	while True:
		wp.pwmWrite(PWM0, 500)
		wp.pwmWrite(PWM1, 500)
		sleep(1)
		wp.pwmWrite(PWM0, 700)
		wp.pwmWrite(PWM1, 700)
		sleep(1)
		wp.pwmWrite(PWM0, 1000)
		wp.pwmWrite(PWM1, 1000)
		sleep(2)
finally:
	wp.pwmWrite(PWM0, OFF)
	wp.pwmWrite(PWM1, OFF)
	wp.pinMode(PWM0, OFF)
	wp.pinMode(PWM1, OFF)
	wp.digitalWrite(PIN2, OFF)
	wp.digitalWrite(PIN1, OFF)
	wp.digitalWrite(PIN3, OFF)
	wp.digitalWrite(PIN4, OFF)
