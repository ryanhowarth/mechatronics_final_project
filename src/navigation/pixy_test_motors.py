#!/usr/bin/python
import NewRobot
from time import sleep

PWM_L = 13
INPUT_1_LEFT = 11
INPUT_2_LEFT = 9

PWM_R = 12
INPUT_1_RIGHT = 25
INPUT_2_RIGHT = 8

SERVO_LIFT = 0
SERVO_PINCH = 7

myRobot = NewRobot.robot(INPUT_1_LEFT, INPUT_2_LEFT, PWM_L, INPUT_1_RIGHT, INPUT_2_RIGHT, PWM_R, SERVO_LIFT, SERVO_PINCH)
	
flag=True
while flag:
  item=myRobot.detectItem()
  print item
  print item
  if item=='gift':
      pickedup=False
      while not pickedup:
        pickedup=myRobot.approachGift()
      dropped=False
      while not dropped:
        if myRobot.detectItem()=='tree':
          dropped=myRobot.approachTree()
          flag=False
  sleep(0.5)
