#!/usr/bin/env python
from time import sleep
import wiringpi as wp
import Motor

#left motor
PWM_R = 12  #pin 32 
INPUT_1_RIGHT = 25 #pin 22
INPUT_2_RIGHT = 8 #pin 24

#right motor
PWM_L = 13 #pin 33
INPUT_1_LEFT = 11 #pin 23 
INPUT_2_LEFT = 9 #pin 21

motorL = Motor.motor(INPUT_1_LEFT, INPUT_2_LEFT, PWM_L)
motorR = Motor.motor(INPUT_1_RIGHT, INPUT_2_RIGHT, PWM_R)

time_turn = .075
time_forward = .2

OFF = 0
def moveRobotForward():
    # Move robot forward one grid space
    motorL.forward()
    motorR.forward()
    print '#########MOVING FORWARD############'

def turnRobotLeft():
    motorL.backward()
    motorR.forward()
    print '#######TURNING LEFT############'

def turnRobotRight():
    # Turn robot 90 degrees right
    motorL.forward()
    motorR.backward()
    print '##########TURNING RIGHT#########'

def turnRobotAround():
    # Turn robot 180 degrees when deadend is found
    turnRobotLeft()
    turnRobotLeft()

def stopMotors():
    motorL.stop()
    motorR.stop()
    
def shutoffRobot():
    wp.pwmWrite(PWM_L, OFF)
    wp.pwmWrite(PWM_R, OFF)
    wp.digitalWrite(INPUT_2_LEFT, OFF)
    wp.digitalWrite(INPUT_1_LEFT, OFF)
    wp.digitalWrite(INPUT_1_RIGHT, OFF)
    wp.digitalWrite(INPUT_2_RIGHT, OFF)
    print 'turn off'

try: 
    motorL.setSpeed(800)
    motorR.setSpeed(800)
    while True:
        print 'begin' 

        moveRobotForward()
        #stopMotors()
        sleep(2)

	turnRobotLeft()
        #stopMotors()
	sleep(2)

	turnRobotRight()
        #stopMotors()
	sleep(2)

	turnRobotAround()
        #stopMotors()
	sleep(2)

finally: 
	shutoffRobot()
