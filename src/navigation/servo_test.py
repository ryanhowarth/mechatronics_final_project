import wiringpi as wp
from time import sleep 
import Adafruit_PCA9685 as ADA

pwm = ADA.PCA9685()

servo_min = 180 #raise
#servo_max = 380 #lower pickup
servo_max = 360 #lower drop
#servo_min = 220 #close
#servo_max = 400 #open
 
PWM_SERVO1 = 0 # raise lower
#PWM_SERVO1 = 7 # open close
pwm.set_pwm_freq(60)

try: 
    while True:
        pwm.set_pwm(PWM_SERVO1, 0, 400)
        for i in xrange(servo_min, servo_max):	
            pwm.set_pwm(PWM_SERVO1,0, i)
        sleep(2)
        
        for i in xrange(servo_min, servo_max):
            pwm.set_pwm(PWM_SERVO1, 0, servo_max + servo_min - i)		
        sleep(2)
finally: 
	pwm.set_pwm(PWM_SERVO1,0, 0)
