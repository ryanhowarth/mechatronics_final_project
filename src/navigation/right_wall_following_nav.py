#!/usr/bin/python
import mapping
from time import sleep 
from pixy import easy_pixy
import NewRobot

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

robot = NewRobot.robot(INPUT_1_LEFT, INPUT_2_LEFT, PWM_L, INPUT_1_RIGHT, INPUT_2_RIGHT, PWM_R, SERVO_LIFT, SERVO_PINCH)

robot.moveForwardUntilNoWall()
