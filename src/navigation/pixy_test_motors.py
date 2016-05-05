#!/usr/bin/python
import NewRobot
from time import sleep

def signal_handler(signal, frame):
    print 'Exiting'
    del robot
    sys.exit(0)

PWM_L = 13
INPUT_1_LEFT = 11
INPUT_2_LEFT = 9

PWM_R = 12
INPUT_1_RIGHT = 25
INPUT_2_RIGHT = 8

SERVO_LIFT = 0
SERVO_PINCH = 7

myRobot = NewRobot.robot(INPUT_1_LEFT, INPUT_2_LEFT, PWM_L, INPUT_1_RIGHT, INPUT_2_RIGHT, PWM_R, SERVO_LIFT, SERVO_PINCH)
	
finished = False
pickedup = False
dropped = False
while not finished:
	item = myRobot.detectItem()
	print item
  	if item == 'gift':
      		while not pickedup:
        		pickedup = myRobot.approachGift()
 	if item == 'tree' and pickedup:
      		while not dropped:
          		dropped = myRobot.approachTree()
		finished = True
