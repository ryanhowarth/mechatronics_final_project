#!/usr/bin/python
from pixy import easy_pixy_test
from time import sleep
from Adafruit_ADS1x15 import ADS1x15
import Claw

pixy_object = easy_pixy_test.easy_pixy()
gift_right=100 #y < _ when gift to right (camera is sideways)
gift_left=120 #y > _ when gift to left
tree_right=100 #y < _ when tree to right (camera is sideways)
tree_left=120 #y > _ when tree to left
gift_far=12.5
gift_near=10.5
tree_far=12.5
gift_near=10.5
front_ir=3

myClaw = Claw.claw(0,7)
irSensor = ADS1x15(ic=0x00)

def irDistLeft(volts):
    return 11.721 * volts**(-0.972)

def pixyDetectItem():
    blocks = pixy_object.get_blocks()
    signature = blocks[0]
    if signature==1:
        return 'tree'
    elif signature==2:
        return 'gift'
    elif signature==0:
        return 'none'
    else:
        return 'other'

# Returns true if pickup or dropoff succesful
def pixyApproach(item):
    x=pixy_object.get_blocks()
    
    if item=='tree':
        v = irSensor.readADCSingleEnded(front_ir,4096,250)/1000
        d = irDistLeft(v)
        while (x[2]<=tree_right or x[2]>=tree_left) or (d<=tree_far or d>=tree_near):
            while x[2]<=tree_right:
                print 'Right'
                x=pixy_object.get_blocks()
            while x[2]>=tree_left:
                print 'Left'
                sleep(0.5)
                x=pixy_object.get_blocks()
            v = irSensor.readADCSingleEnded(front_ir,4096,250)/1000
            d = irDistLeft(v)
            print d
#            if d<tree_far and d>tree_near:
#                break
            while d >= tree_far:
                print 'Forward'
                sleep(0.25)
                v = irSensor.readADCSingleEnded(front_ir,4096,250)/1000
                d = irDistLeft(v)
#                print d

            while d<=tree_near:
                print 'Back'
                sleep(0.25)
                v = irSensor.readADCSingleEnded(front_ir,4096,250)/1000
                d = irDistLeft(v)
#                print d

            x=pixy_object.get_blocks()
            sleep(0.5)
        print 'Reached dropoff location'
        myClaw.dropGift()
        return True
    elif item=='gift':
        v = irSensor.readADCSingleEnded(front_ir,4096,250)/1000
        d = irDistLeft(v)
        while (x[2]<=gift_right or x[2]>=gift_left) or (d<=gift_far or d>=gift_near):
            while x[2]<=gift_right:
                print 'Right'
                x=pixy_object.get_blocks()
            while x[2]>=gift_left:
                print 'Left'
                x=pixy_object.get_blocks()
            v = irSensor.readADCSingleEnded(front_ir,4096,250)/1000
            d = irDistLeft(v)
            print d
            if d<gift_far and d>gift_near:
                break
            if d>=gift_far:
                print 'Forward'
            if d<=gift_near:
                print 'Back'
            x=pixy_object.get_blocks()
            sleep(0.5)
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
