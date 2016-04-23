#!/usr/bin/env python
from time import sleep
import wiringpi as wp

#left motor
PWM_L = 12  #pin 32 
INPUT_1_LEFT = 8 #pin 24
INPUT_2_LEFT = 25 #pin 22

#right motor
PWM_R = 13 #pin 33
INPUT_1_RIGHT = 11 #pin 23 
INPUT_2_RIGHT = 9 #pin 21

motorL = motor(INPUT_1_LEFT, INPUT_2_LEFT, PWM_L)
motorR = motor(INPUT_1_RIGHT, INPUT_2_RIGHT, PWM_R)


time_turn = .075
time_forward = .2

wp.wiringPiSetupGpio()
def moveRobotForward():
    # Move robot forward one grid space
    motorL.forward()
    motorR.forward()
    print '#########MOVING FORWARD############'
    sleep(1)

def turnRobotLeft():
    motorL.backward()
    motorR.forward()
    print '#######TURNING LEFT############'
    sleep(1)

def turnRobotRight():
    # Turn robot 90 degrees right
    motorL.forward()
    motorR.backward()
    print '##########TURNING RIGHT#########'
    sleep(1)

def turnRobotAround():
    # Turn robot 180 degrees when deadend is found
    print 'turn around'
    turnRobotLeft()
    turnRobotLeft()

def stopMotors():
    motorL.stop()
    motorR.stop()
    
def shutoffRobot():
    wp.pwmWrite(PWM_L, OFF)
    wp.pwmWrite(PWM_R, OFF)
    wp.digitalWrite(INPUT_2_LEFT_MOTOR, OFF)
    wp.digitalWrite(INPUT_1_LEFT_MOTOR, OFF)
    wp.digitalWrite(INPUT_1_RIGHT_MOTOR, OFF)
    wp.digitalWrite(INPUT_2_RIGHT_MOTOR, OFF)
    print 'turn off'

try: 
    motorL.setSpeed(500)
    motorR.setSpeed(500)
    while True:
        print 'begin' 

        moveRobotForward()
        stopMotors()
        sleep(2)

		turnRobotLeft()
        stopMotors()
		sleep(2)

		turnRobotRight()
        stopMotors()
		sleep(2)

		turnRobotAround()
        stopMotors()
		sleep(2)

finally: 
	shutoffRobot()
