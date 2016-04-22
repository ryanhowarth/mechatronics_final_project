#!/usr/bin/env python
from time import sleep
import wiringpi as wp

#left motor
PWM_L = 12  #pin 32
INPUT_1_LEFT_MOTOR = 8 #pin 24
INPUT_2_LEFT_MOTOR = 25 #pin 22

#right motor
PWM_R = 13 #pin 33
INPUT_1_RIGHT_MOTOR = 11 #pin 23
INPUT_2_RIGHT_MOTOR = 9 #pin 21

PWM_MODE = 2
ON = 1
OFF = 0

time_turn = .075
time_forward = .2

wp.wiringPiSetupGpio()

#enable PWM_L
wp.pinMode(PWM_L, PWM_MODE)  #set pin to pwm mode
wp.pwmWrite(PWM_L, OFF)

#enable PWM_R
wp.pinMode(PWM_R, PWM_MODE)
wp.pwmWrite(PWM_R, OFF)

#enable pins motor1 -- Lmotor
wp.pinMode(INPUT_1_LEFT_MOTOR, 1)
wp.pinMode(INPUT_2_LEFT_MOTOR, 1)

#enable pins motor2 -- Rmotor
wp.pinMode(INPUT_1_RIGHT_MOTOR,1)
wp.pinMode(INPUT_2_RIGHT_MOTOR,1)

def forwardLmotor():
    wp.digitalWrite(INPUT_1_LEFT_MOTOR, OFF)
    wp.digitalWrite(INPUT_2_LEFT_MOTOR, ON)

def backwardLmotor():
    wp.digitalWrite(INPUT_1_LEFT_MOTOR, ON)
    wp.digitalWrite(INPUT_2_LEFT_MOTOR, OFF)

def forwardRmotor():
    wp.digitalWrite(INPUT_1_RIGHT_MOTOR, OFF)
    wp.digitalWrite(INPUT_2_RIGHT_MOTOR, ON)

def backwardRmotor():
    wp.digitalWrite(INPUT_1_RIGHT_MOTOR, ON)
    wp.digitalWrite(INPUT_2_RIGHT_MOTOR, OFF)

def moveRobotForward():
    # Move robot forward one grid space
    print ' forward'
    forwardRmotor()
    forwardLmotor()
    wp.pwmWrite(PWM_L, 1024)
    wp.pwmWrite(PWM_R, 1024)
    sleep(5)
    #wp.pwmWrite(PWM_L, 0)
    #wp.pwmWrite(PWM_R, 0)
   

def turnRobotLeft():
    # Turn robot 90 degrees left
    print 'left'
    forwardRmotor()
    backwardLmotor()
    wp.pwmWrite(PWM_L, 1024)
    wp.pwmWrite(PWM_R, 1024)
    sleep(time_turn)
    wp.pwmWrite(PWM_R, 0)
    wp.pwmWrite(PWM_L, 0)
    


def turnRobotRight():
    # Turn robot 90 degrees right
    print 'right' 
    forwardLmotor()
    backwardRmotor()
    wp.pwmWrite(PWM_L, 1024)
    wp.pwmWrite(PWM_R, 1024)
    sleep(time_turn)
    wp.pwmWrite(PWM_L, 0)
    wp.pwmWrite(PWM_R, 0)
    
   

def turnRobotAround():
    # Turn robot 180 degrees when deadend is found
    print 'turn around'
    turnRobotLeft()
    turnRobotLeft()
    

def shutoffRobot():
    wp.pwmWrite(PWM_L, OFF)
    wp.pwmWrite(PWM_R, OFF)
    wp.digitalWrite(INPUT_2_LEFT_MOTOR, OFF)
    wp.digitalWrite(INPUT_1_LEFT_MOTOR, OFF)
    wp.digitalWrite(INPUT_1_RIGHT_MOTOR, OFF)
    wp.digitalWrite(INPUT_2_RIGHT_MOTOR, OFF)
    print 'turn off'

try: 
    while True:
	print 'starting code' 
	moveRobotForward()
	break	#sleep(2.0)
		#turnRobotLeft()
		#sleep(2.0)
		#moveRobotForward()
		#sleep(2.0)
		#turnRobotRight()
		#sleep(2.0)
		#moveRobotForward()
		#sleep(2.0)
		#turnRobotAround()
		#sleep(2.0)

finally: 
	shutoffRobot()
