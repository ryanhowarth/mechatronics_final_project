import wiringpi as wp
from time import sleep 
import Adafruit_PCA9685 as ADA

pwm = ADA.PCA9685()

servo1_min = 180 #raise
servo1_max = 380 #lower pickup
#servo_max = 360 #lower drop
servo2_min = 250 #close
servo2_max = 400 #open
 
PWM_SERVO1 = 0 # raise lower
PWM_SERVO2 = 7 # open close
pwm.set_pwm_freq(60)

try: 
    pwm.set_pwm(PWM_SERVO1, 0, 400)
    pwm.set_pwm(PWM_SERVO2, 0, 400)
    while True:
        #pwm.set_pwm(PWM_SERVO1, 0, 170)
        for i in xrange(servo1_min, servo1_max):	
            pwm.set_pwm(PWM_SERVO1,0, i)
        sleep(1)

        for j in xrange(servo2_min, servo2_max):	
            pwm.set_pwm(PWM_SERVO2,0, j)
        sleep(1)
        
        for j in xrange(servo2_min, servo2_max):
            pwm.set_pwm(PWM_SERVO2, 0, servo2_max + servo2_min - j)
	sleep(1)
        
        for i in xrange(servo1_min, servo1_max):
            pwm.set_pwm(PWM_SERVO1, 0, servo1_max + servo1_min - i)
	sleep(1)
finally: 
	pwm.set_pwm(PWM_SERVO1,0, 0)
	pwm.set_pwm(PWM_SERVO2,0, 0)
