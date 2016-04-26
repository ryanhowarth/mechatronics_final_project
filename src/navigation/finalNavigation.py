#!/usr/bin/python
import mapping
from time import sleep 
from pixy import easy_pixy
import Robot

import signal
import sys

def signal_handler(signal, frame):
    print 'Exiting'
    del robot
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#Pixy 
#pixy_object = easy_pixy.easy_pixy()

#left motor
PWM_L = 12  #pin 32 
INPUT_1_LEFT = 8 #pin 24
INPUT_2_LEFT = 25 #pin 22

#right motor
PWM_R = 13 #pin 33
INPUT_1_RIGHT = 11 #pin 23 
INPUT_2_RIGHT = 9 #pin 21

SERVO_LIFT = 0
SERVO_PINCH = 7

robot = Robot.robot(INPUT_1_LEFT, INPUT_2_LEFT, PWM_L, INPUT_1_RIGHT, INPUT_2_RIGHT, PWM_R, SERVO_LIFT, SERVO_PINCH)

def update_intersection(robot):
	distances = robot.getIrSensorData()

	path_lst=[False]*3

	path_lst[0] = distances[0] > 20
	path_lst[1] = distances[1] > 20
	path_lst[2] = distances[2] > 20
	
	return path_lst 

def checkItem():
	# Check if there's an item
	itemFound = pixyDetectItem()

	if itemFound == 'gift':
		giftFound = True
		pickUpGift()

		if treeFound: 
			# Exit and navigate to the tree
		    pass

	elif itemFound == 'tree':
		treeFound = True

		if giftFound:
			dropGift()
			giftDropped = True
			
		turnList = {1: 'G'}
		turnIndex = 2

def pixyDetectItem():

	item = ''

	if digitalRead(TREE_PIN):
		item = 'tree'
	elif digitalRead(GIFT_PIN):
		item = 'gift'

	return item

# Initialize first node
map_dic={1:[[0,0,0],[0,0,0],0,'N']}

# Initialize tree_lst: current = 1, previous = 0, highest index = 1, direction = forward
tree_lst=[1,0,1,'f']

# Initialize path_lst: assume facing forward at start
path_lst=[False,True,False] 

# Initialize that tree and gift have not been found
giftFound = False
treeFound = False
giftDropped = False

# Create second node based on initialized tree_lst and path_lst
mapping.node_proc(map_dic, tree_lst, path_lst)

# Print current structure
mapping.print_node(map_dic)

while True:
	sleep(.5)
	robot.moveForward()

	path_lst = update_intersection(irSensors)

	# Check if left turn is available
	if path_lst[0]:
		robot.turnLeft()
		
		# If at an intersection, add node to structure
		if path_lst[1] or path_lst[2]:
			mapping.node_proc(map_dic, tree_lst, path_lst)

		# Mark opposite turn if tree is found
		if treeFound:
			if tree_lst[2]:
				turnList[turnIndex] = 'R'
				turnIndex += 1
			else:
				turnIndex -= 1
				del turnList[turnIndex]

	# Check if straight is available
	elif path_lst[1]:
		# Keep robot straight

		if path_lst[2]:
			mapping.node_proc(map_dic, tree_lst, path_lst)

		# Mark middle if tree is found
		if treeFound:
			if tree_lst[2] == 'f':
				turnList[turnIndex] = 'M'
				turnIndex += 1
			else:
				turnIndex -= 1
				del turnList[turnIndex]

	# Check if right is available
	elif path_lst[2]:
		robot.turnRight()

		# Mark opposite turn if tree is found
		if treeFound:
			if tree_lst[2]:
				turnList[turnIndex] = 'L'
				turnIndex += 1
			else:
				turnIndex -= 1
				del turnList[turnIndex]

	# Deadend has been reached
	else:

		robot.turnAround()

		# Swap current node and previous node
		temp = tree_lst[1]
		tree_lst[1] = tree_lst[0]
		tree_lst[0] = temp

		# Change direction
		tree_lst[2] = 'b'



