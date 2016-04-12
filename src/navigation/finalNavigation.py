#!/usr/bin/python

import mapping
#from Adafruit_ADS1x15 import ADS1x15

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

    gain = 4096
    sps = 250

    voltsL = sensorL.readADCSingleEnded(0,gain,sps)/1000
    distanceL = irDistFunction(voltsL)
    
    voltsM = sensorM.readADCSingleEnded(1,gain,sps)/1000
    distanceM = irDistFunction(voltsM)
    
    voltsR = sensorR.readADCSingleEnded(2,gain,sps)/1000
    distanceR = irDistFunction(voltsR)

    path_lst=[False]*3

    path_lst[0] = distanceL > 5
    path_lst[1] = distanceM > 5
    path_lst[2] = distanceR > 5
    
    return path_lst 

def irDistFunction(volts):
    # Function to calculate distance from sensor input
    ''' TODO: Calibrate for specific sensor '''
    return 12.374 * volts**(-1.09)

def pixyDetectItem():
    # Insert pixy code here
    # return 'gift' if gift is detected, 'tree' if tree is detected, else ''
    return ''

def pickUpGift():
    # Pick up the gift
    pass

def dropGift():
    # Drop the gift at the tree
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
giftDropped = False

# Initialize sensors
sensorL=ADS1x15(ic=ADS1015)
sensorM=ADS1x15(ic=ADS1015)
sensorR=ADS1x15(ic=ADS1015)

''' TODO: Initialize Pixy '''

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
        turnRobotRight()

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

        # Check if there's an item
        itemFound = pixyDetectItem()

        if itemFound == 'gift':
            giftFound = True
            pickUpGift()

            if treeFound: 
                # Exit and navigate back to tree
                turnRobotAround()
                break

        elif itemFound == 'tree':
            treeFound = True

            if giftFound:
                dropGift()
                giftDropped = True
                break
            
            turnList = {1: 'G'}
            turnIndex = 2

        # Swap current node and previous node
        temp = tree_lst[1]
        tree_lst[1] = tree_lst[0]
        tree_lst[0] = temp

        # Change direction
        tree_lst[2] = 'b'

        turnRobotAround()


while not giftDropped:

    moveRobotForward()

    # Access previous turn
    turnIndex -= 1
    currTurn = turnList[turnIndex]

    # Turn depending on last command. Drop gift
    if currTurn == 'L':
        turnRobotLeft()
    elif currTurn == 'R':
        turnRobotRight()
    elif currTurn == 'G':
        dropGift()



