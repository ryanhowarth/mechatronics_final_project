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

robot = Robot.robot(INPUT_1_LEFT, INPUT_2_LEFT, PWM_L, INPUT_1_RIGHT, INPUT_2_RIGHT, PWM_R, SERVO_LIFT, SERVO_PINCH)

def update_intersection(robot):
	distances = robot.getIrSensorData()

	path_lst=[False]*3
	for i in xrange(3):
	    path_lst[i] = distances[i] > 20
	
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

mapping.node_proc(map_dic, tree_lst, path_lst)

# Initialize that tree and gift have not been found
giftFound = False
treeFound = False
giftDropped = False

# Create second node based on initialized tree_lst and path_lst
mapping.node_proc(map_dic, tree_lst, path_lst)

# Print current structure
mapping.print_node(map_dic)

prev_decision = 0

while True:
	sleep(1)
	robot.moveForward(prev_decision)
	
	path_lst = update_intersection(robot)

	# Check if left turn is available
	if path_lst[0]:
		if path_lst[2]:
			wall = 1
		else:
			wall = 2
		robot.step_forward(wall)

		robot.turnLeft()
		prev_decision = 0
		# If at an intersection, add node to structure
		if path_lst[1] or path_lst[2]:
			mapping.node_proc(map_dic, tree_lst, path_lst)

		# Mark opposite turn if tree is found
		if treeFound:
			if tree_lst[3]=='f':
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
			if tree_lst[3] == 'f':
				turnList[turnIndex] = 'M'
				turnIndex += 1
			else:
				turnIndex -= 1
				del turnList[turnIndex]

	# Check if right is available
	elif path_lst[2]:
		wall = 0
		robot.step_forward(wall)

		robot.turnRight()
		prev_decision = 2

		# Mark opposite turn if tree is found
		if treeFound:
			if tree_lst[3]=='b':
				turnList[turnIndex] = 'L'
				turnIndex += 1
			else:
				turnIndex -= 1
				del turnList[turnIndex]

	# Deadend has been reached
	else:

		robot.turnAround()
		prev_decision = -1
		# Swap current node and previous node
		temp = tree_lst[1]
		tree_lst[1] = tree_lst[0]
		tree_lst[0] = temp

		# Change direction
		tree_lst[3] = 'b'
	#robot.step_forward()
