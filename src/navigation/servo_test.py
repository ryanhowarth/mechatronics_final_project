import wiringpi as wp
from time import sleep 
import Adafruit_PCA9685 as ADA

pwm = ADA.PCA9685()

servo_min = 260
servo_max = 400
 
PWM_SERVO1 = 7  

pwm.set_pwm_freq(60)

try: 
    while True:
        for i in xrange(servo_min, servo_max):	
            pwm.set_pwm(PWM_SERVO1,0, i)
        sleep(2)
        
        for i in xrange(servo_min, servo_max):
            pwm.set_pwm(PWM_SERVO1, 0, servo_max + servo_min - i)		
        sleep(2)
finally: 
	pwm.set_pwm(PWM_SERVO1,0, 0)
