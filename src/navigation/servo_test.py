import wiringpi as wp
from time import sleep 

wp.wiringPiSetupGpio()
 
PWM_SERVO1 = 12 #pin 32
PWM_SERVO2 = 13 #pin 33
PWM_MODE = 2

wp.pinMode(PWM_SERVO1, PWM_MODE)
wp.pwmSetMode(0)
wp.pwmSetClock(400)
wp.pwmSetRange(1024)
wp.pwmWrite(PWM_SERVO1, 1000)

wp.pinMode(PWM_SERVO2, PWM_MODE)
wp.pwmSetMode(0)
wp.pwmSetClock(400)
wp.pwmSetRange(1024)

try: 
	while True:
		print '128'
		wp.pwmWrite(PWM_SERVO2, 128)
		sleep(2)
		print '63'
		wp.pwmWrite(PWM_SERVO2, 80)		
		sleep(2)

finally: 
	wp.pwmWrite(PWM_SERVO2, 0)
