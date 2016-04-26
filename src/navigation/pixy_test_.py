#!/usr/bin/python
from pixy import easy_pixy_test
from time import sleep
from Adafruit_ADS1x15 import ADS1x15
import Claw

pixy_object = easy_pixy_test.easy_pixy()
gift_right=140 #y < _ when gift to right (camera is sideways)
gift_left=170 #y > _ when gift to left
#gift_near=250 #x > _ when gift too close
#gift_far=240 #x < _ when gift too far
tree_right=140 #y < _ when tree to right (camera is sideways)
tree_left=170 #y > _ when tree to left
#tree_near=250 #x > _ when tree too close
#tree_far=240 #x < _ when tree too far
far=5.5
near=5.3
front_ir=1

myClaw = Claw.claw(0,7)
irSensor = ADS1x15(ic=0x00)

def irDistLeft(volts):
    return 11.721 * volts**(-0.972)

def pixyDetectItem():
    x = pixy_object.get_blocks_and_print()
    if x[0]==1:
        return 'tree'
    elif x[0]==2:
        return 'gift'
    elif x[0]==0:
        return 'none'
    else:
        return 'other'

# Returns true if pickup or dropoff succesful
def pixyApproach(item):
    x=pixy_object.get_blocks()
    
    if item=='tree':
        v = irSensor.readADCSingleEnded(front_ir,4096,250)/1000
        d = irDistLeft(v)
        while (x[2]<=tree_right or x[2]>=tree_left) or (d<=far or d>=near):
            while x[2]<=tree_right:
                print 'R'
                x=pixy_object.get_blocks()
            while x[2]>=tree_left:
                print 'L'
                x=pixy_object.get_blocks()
            v = irSensor.readADCSingleEnded(front_ir,4096,250)/1000
            d = irDistLeft(v)
            if d<far and d>near:
                break
            if d>=far:
                print 'F'
            if d<=near:
                print 'B'
            x=pixy_object.get_blocks()
 #       '''    
 #       while x[2]<=tree_right or x[2]>=tree_left:
 #           # adjust L/R until tree is in center (slowly)
 #           if x[2]<=tree_right:
 #               #move right
 #               print 'move right'
 #           elif x[2]>=tree_left: 
 #               #move left
 #               print 'move left'
 #           x=pixy_object.get_blocks()
 #       while x[1]<=tree_far or x[1]>=tree_near:
 #           if x[1]<=tree_far:
 #               #move forward
 #               print 'move forward'
 #           elif x[1]>=tree_far:
 #               #move back
 #               print 'move back'
 #           x=pixy_object.get_blocks()
 #       '''
        print 'Reached dropoff location'
        myClaw.dropGift()
        return True
    elif item=='gift':
        v = irSensor.readADCSingleEnded(front_ir,4096,250)/1000
        d = irDistLeft(v)
        while (x[2]<=gift_right or x[2]>=gift_left) or (d<=far or d>=near):
            while x[2]<=gift_right:
                print 'R'
                x=pixy_object.get_blocks()
            while x[2]>=gift_left:
                print 'L'
                x=pixy_object.get_blocks()
            v = irSensor.readADCSingleEnded(front_ir,4096,250)/1000
            d = irDistLeft(v)
            if d<far and d>near:
                break
            if d>=far:
                print 'F'
            if d<=near:
                print 'B'
            x=pixy_object.get_blocks()
#        '''
#        while x[2]<=gift_right or x[2]>=gift_left:
#            # adjust L/R until gift is in center (slowly)
#            if x[2]<=gift_right:
#                #move right
#                print 'move right'
#            elif x[2]>=gift_left: 
#                #move left
#                print 'move left'
#            x=pixy_object.get_blocks()
#        while x[1]<=gift_far or x[1]>=gift_near:
#            if x[1]<=gift_far:
#                #move forward
#                print 'move forward'
#            elif x[1]>=gift_far:
#                #move back
#                print 'move back'
#            x=pixy_object.get_blocks()
#        '''
        print 'Reached pickup location'
        myClaw.pickupGift()
	return True

flag=True
while flag:
  item=pixyDetectItem()
  print item
  if item=='gift':
      pickedup=False
      while not pickedup:
        pickedup=pixyApproach('gift')
      dropped=False
      while not dropped:
        if pixyDetectItem()=='tree':
          dropped=pixyApproach('tree')
          flag=False
  sleep(0.5)
