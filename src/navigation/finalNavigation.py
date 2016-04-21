#!/usr/bin/python

import mapping
from Adafruit_ADS1x15 import ADS1x15
import wiringpi as wp
from time import sleep 
from pixy import easy_pixy
import Adafruit_PCA9685

#Pixy 
pixy_object = easy_pixy.easy_pixy()

#pwm
servoControl = Adafruit_PCA9685.PCA9685()

#left motor
PWM_L = 12  #pin 32 
INPUT_1_LEFT_MOTOR = 25 #pin 22
INPUT_2_LEFT_MOTOR = 8 #pin 24

#right motor
PWM_R = 13 #pin 33
INPUT_1_RIGHT_MOTOR = 9 #pin 21 
INPUT_2_RIGHT_MOTOR = 11 #pin 23

time_turn = .15
time_forward = .4

GIFT_PIN = 20 #pin 38
TREE_PIN = 21 #pin 21

SERVO_LIFT = 0
SERVO_PINCH = 7

LOWER_SERVO = 175
RAISE_SERVO = 400
OPEN_SERVO = 400
CLOSE_SERVO = 260

servoControl.set_pwm(SERVO_LIFT, 0, RAISE_SERVO)
servoControl.set_pwm(SERVO_PINCH, 0, CLOSE_SERVO)

INPUT_MODE = 0
OUTPUT_MODE = 1
PWM_MODE = 2

wp.wiringPiSetupGpio()

#enable PWM_L
wp.pinMode(PWM_L, PWM_MODE)  #set pin to pwm mode
wp.pwmWrite(PWM_L, 0)

#enable PWM_R
wp.pinMode(PWM_R, PWM_MODE)
wp.pwmWrite(PWM_R, 0)

#enable pins motor1 -- Lmotor
wp.pinMode(INPUT_1_LEFT_MOTOR, OUTPUT_MODE)
wp.pinMode(INPUT_2_LEFT_MOTOR, OUTPUT_MODE)

#enable pins motor2 -- Rmotor
wp.pinMode(INPUT_1_RIGHT_MOTOR, OUTPUT_MODE)
wp.pinMode(INPUT_2_RIGHT_MOTOR, OUTPUT_MODE)

wp.pinMode(GIFT_PIN, INPUT_MODE)
wp.pinMode(TREE_PIN, INPUT_MODE)

wp.pinMode(12, PWM_MODE)
wp.pinMode(13, PWM_MODE)
wp.pwmSetMode(0)
wp.pwmSetClock(400)
wp.pwmSetRange(1024)
wp.pwmWrite(12,0)
wp.pwmWrite(13,0) 

def forwardLmotor():
    wp.digitalWrite(INPUT_1_LEFT_MOTOR, 0)
    wp.digitalWrite(INPUT_2_LEFT_MOTOR, 1)

def backwardLmotor():
    wp.digitalWrite(INPUT_1_LEFT_MOTOR, 1)
    wp.digitalWrite(INPUT_2_LEFT_MOTOR, 0)

def forwardRmotor():
    wp.digitalWrite(INPUT_1_RIGHT_MOTOR, 0)
    wp.digitalWrite(INPUT_2_RIGHT_MOTOR, 1)

def backwardRmotor():
    wp.digitalWrite(INPUT_1_RIGHT_MOTOR, 1)
    wp.digitalWrite(INPUT_2_RIGHT_MOTOR, 0)

def moveRobotForward():
    # Move robot forward one grid space
    forwardRmotor()
    forwardLmotor()
    wp.pwmWrite(PWM_L, 600)
    wp.pwmWrite(PWM_R, 600)
    sleep(time_forward)
    wp.pwmWrite(PWM_L, 0)
    wp.pwmWrite(PWM_R, 0)
    print 'forward'

def turnRobotLeft():
    # Turn robot 90 degrees left
    forwardRmotor()
    backwardLmotor()
    wp.pwmWrite(PWM_L, 600)
    wp.pwmWrite(PWM_R, 600)
    sleep(time_turn)
    wp.pwmWrite(PWM_R, 0)
    wp.pwmWrite(PWM_L, 0)
    print 'turn left'

def turnRobotRight():
    # Turn robot 90 degrees right
    forwardLmotor()
    backwardRmotor()
    wp.pwmWrite(PWM_L, 600)
    wp.pwmWrite(PWM_R, 600)
    sleep(time_turn)
    wp.pwmWrite(PWM_L, 0)
    wp.pwmWrite(PWM_R, 0)
    print 'turn right'


def turnRobotAround():
    # Turn robot 180 degrees when deadend is found
    turnRobotLeft()
    turnRobotLeft()
    print 'turn around'

def shutoffRobot():
    wp.pwmWrite(PWM_L, 0)
    wp.pwmWrite(PWM_R, 0)
    wp.digitalWrite(INPUT_2_LEFT_MOTOR, 0)
    wp.digitalWrite(INPUT_1_LEFT_MOTOR, 0)
    wp.digitalWrite(INPUT_1_RIGHT_MOTOR, 0)
    wp.digitalWrite(INPUT_2_RIGHT_MOTOR, 0)
    print 'turn off'

def update_intersection(irSensors):
    # Check surroundings for available paths
    gain = 4096
    sps = 250
    distanceL=[]
    distanceM = []
    distanceR = []

    for i in xrange(1, 10):
        voltsL = irSensors.readADCSingleEnded(0,gain,sps)/1000
        distanceL.append(irDistLeft(voltsL))
	voltsM = irSensors.readADCSingleEnded(1,gain,sps)/1000
        distanceM.append(irDistFront(voltsM))
	voltsR = irSensors.readADCSingleEnded(2,gain,sps)/1000
        distanceR.append( irDistRight(voltsR))
	sleep(.1)

    final_distanceL = sum(distanceL)/len(distanceL)
    final_distanceM = sum(distanceM)/len(distanceM)
    final_distanceR = sum(distanceR)/len(distanceR)    
    print 'left: ' + str(final_distanceL)
    
    print 'front: ' + str(final_distanceM)
    
    print 'right: ' + str(final_distanceR)

    path_lst=[False]*3

    path_lst[0] = final_distanceL > 20
    path_lst[1] = final_distanceM > 20
    path_lst[2] = final_distanceR > 20
    
    return path_lst 

''' 
*** NOTE ***
Left: Dark Green 2Y0A21
Front: 2D120X
Right: Light Green 2Y0A21
'''

def irDistLeft(volts):
    # Function to calculate distance from right sensor
    return 26.47 * volts**(-1.185)

def irDistFront(volts):
    return 11.721 * volts**(-0.972)

def irDistRight(volts):
    # Function to calculate distance from left sensor
    return 26.453 * volts**(-1.221)

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
            k
            
        turnList = {1: 'G'}
        turnIndex = 2

def pixyDetectItem():

    item = ''

    if digitalRead(TREE_PIN):
        item = 'tree'
    elif digitalRead(GIFT_PIN):
        item = 'gift'

    return item

def pickUpGift():
    print 'picking up'
    servoControl.set_pwm(SERVO_PINCH, 0, OPEN_SERVO)
    sleep(1)
    servoControl.set_pwm(SERVO_LIFT, 0, LOWER_SERVO)
    sleep(1)
    servoControl.set_pwm(SERVO_PINCH,0, CLOSE_SERVO)
    sleep(1)
    servoControl.set_pwm(SERVO_LIFT, 0, RAISE_SERVO)
    sleep(1)

def dropGift():
    print 'dropping'
    servoControl.set_pwm(SERVO_LIFT, 0, LOWER_SERVO)
    sleep(1)
    servoControl.set_pwm(SERVO_PINCH, 0, OPEN_SERVO)
    sleep(1)
    servoControl.set_pwm(SERVO_LIFT, 0, RAISE_SERVO)
    sleep(1)
    servoControl.set_pwm(SERVO_PINCH, 0, CLOSE_SERVO)
    sleep(1)
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
irSensors = ADS1x15(ic=0x00)

# Create second node based on initialized tree_lst and path_lst
mapping.node_proc(map_dic, tree_lst, path_lst)

# Print current structure
mapping.print_node(map_dic)

while True:
    #pwmControl.set_pwm(0,0,150)
    sleep(3)
    moveRobotForward()
    #pwmControl.set_pwm(0,0,600)
    path_lst = update_intersection(irSensors)

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

        # Swap current node and previous node
        temp = tree_lst[1]
        tree_lst[1] = tree_lst[0]
        tree_lst[0] = temp

        # Change direction
        tree_lst[2] = 'b'



