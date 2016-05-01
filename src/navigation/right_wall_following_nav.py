#!/usr/bin/python
import mapping
from time import sleep 
from pixy import easy_pixy
import NewRobot

import signal
import sys
import IrSensor



 
def signal_handler(signal, frame):
    print 'Exiting'
    del robot
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


#irsensor object
irSensors = IrSensor.irSensor()
IR_LEFT = 0
IR_MIDDLE = 1
IR_RIGHT = 2

#Pixy 
#pixy_object = easy_pixy.easy_pixy()

#Right  motor
PWM_R = 12  #pin 32 
INPUT_1_RIGHT = 25 #pin 22
INPUT_2_RIGHT = 8 #pin 24

#right motor
PWM_L = 13 #pin 33
INPUT_1_LEFT = 11 #pin 23 
INPUT_2_LEFT = 9 #pin 21

SERVO_LIFT = 0
SERVO_PINCH = 7

robot = NewRobot.robot(INPUT_1_LEFT, INPUT_2_LEFT, PWM_L, INPUT_1_RIGHT, INPUT_2_RIGHT, PWM_R, SERVO_LIFT, SERVO_PINCH)

sleep_time = 1.5
THRESH = 17


#########################################################################
################ Function that makes navigation decisions################
#########################################################################

#Looks at IR Data and commands the robot.
def process_ir_data():
	irData = irSensors.getIrSensorData()
	print "irData: ", irData

	#If both the middle and right paths are blocked the robot turns left.
	#If the robot hits a dead end then this will get called twice.
	if irData[IR_RIGHT] < THRESH and irData[IR_MIDDLE] < THRESH:
		print "TURN LEFT"
		robot.turnLeft()
		sleep(sleep_time)

	#if the right path is open turn right (Always following right wall)
	elif irData[IR_RIGHT] > THRESH:
		print "TURN RIGHT"
		robot.turnRight()
		sleep(sleep_time)
		print "FIND RIGHT WALL"
		robot.moveForwardToFindRightWall()
		sleep(sleep_time)
	
	#right wall blocked but middle wall open.
	#goes until the right wall is blocked or middle wall blocks the robot.
	#moveForwardUntilNoWall returns false when it is blocked by middle wall.
	#if it returns true, the robot turns right and tries to find the right
	#wall again.
	elif irData[IR_RIGHT] < THRESH and irData[IR_MIDDLE] > THRESH:
		if (robot.moveForwardUntilNoWall()):
			print "TIL NO WALL"
			sleep(sleep_time)
			print "CLEAR RADIUS"
			robot.moveForwardToClearTurnRadius()
			sleep(sleep_time)
			print "TURN RIGHT"
			robot.turnRight()
			sleep(sleep_time)
			print "FIND RIGHT WALL"
			robot.moveForwardToFindRightWall()
			sleep(sleep_time)
		sleep(sleep_time)
	
	
#robot.turnLeft()
#robot.stop()
#sleep(1)
#robot.turnRight()
	
case = 1
try:
	#Starting motions
	robot.moveForwardUntilNoWall()
	robot.moveForwardToClearTurnRadius()
	#Run until ctrl-c
	while 1:
		process_ir_data()		
finally:
	robot.stop()




		
