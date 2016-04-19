import wiringpi as wp
from time import sleep

#left pins
PWM_L = 23 #pin 33
INPUT1_L = 24 #pin 35
INPUT2_L = 25 #pin 37

#right pins
PWM_R = 26 #pin 32
INPUT1_R = 27 #pin 36
INPUT2_R = 28 #pin 38 
 
PWM_MODE = 2

wp.wiringPiSetupGpio()

#enable PWM_R
wp.pinMode(PWM_R, PWM_MODE)  #set pin to pwm mode
wp.pwmWrite(PWM_R, OFF)

#enable PWM_L
wp.pinMode(PWM_L, PWM_MODE)
wp.pwmWrite(PWM_L, OFF)

#enable pins motor1
wp.pinMode(PIN1, 1)
wp.pinMode(PIN2, 1)
wp.digitalWrite(PIN1, ON)
wp.digitalWrite(PIN2, OFF)

#enable pins motor2
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
