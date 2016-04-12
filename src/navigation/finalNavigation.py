#!/usr/bin/python

import numpy as np
import time
import cv2
import mapping

def moveRobotForward():
    # Move robot forward one grid space
    pass

def turnRobotLeft():
    # Turn robot 90 degrees left
    pass

def turnRobotRight():
    # Turn robot 90 degrees right
    pass

def turnRobotAround():
    # Turn robot 180 degrees when deadend is found
    turnRobotLeft()
    turnRobotLeft()

def update_intersection(sensorL, sensorM, sensorR):
    # Check surroundings for available paths
    path_lst = [False]*3
    return path_lst

def pickUpGift():
    # Pick up the gift
    pass

# Initialize first node
map_dic={1:[[0,0,0],[0,0,0],0,'N']}

# Initialize tree_lst: current = 1, previous = 0, highest index = 1, direction = forward
tree_lst=[1,0,1,'f']

# Initialize path_lst: assume facing forward at start
path_lst=[False,True,False] 

# Initialize that tree and gift have not been found
giftFound = False
treeFound = False

''' TODO: Initialize sensors '''
sensorL = 0
sensorM = 0
sensorR = 0

# Create second node based on initialized tree_lst and path_lst
mapping.node_proc(map_dic, tree_lst, path_lst)

# Print current structure
mapping.print_node(map_dic)

while True:

    moveRobotForward()

    path_lst = update_intersection(sensorL, sensorM, sensorR)

    # Check if left turn is available
    if path_lst[0]:
        turnRobotLeft()

        # If at an intersection, add node to structure
        if path_lst[1] or path_lst[2]:
            mapping.node_proc(map_dic, tree_lst, path_lst)

    # Check if straight is available
    elif path_lst[1]:
        # Keep robot straight here

        if path_lst[2]:
            mapping.node_proc(map_dic, tree_lst, path_lst)

    # Check if right is available
    elif path_lst[2]:
        turnRobotRight()

    # Deadend has been reached
    else:

        # Insert Pixy code here
        if giftFound:
            pickUpGift()

            if treeFound: 
                # Navigate back to tree
                pass

        elif treeFound:
            # Begin tracking turns to get back to tree
            pass



