#!/usr/bin/python
from pixy import easy_pixy_test
from time import sleep

pixy_object = easy_pixy_test.easy_pixy()
gift_left=160 #y < 160 when gift to left (camera is sideways)
gift_right=180 #y > 180 when gift to right
gift_near=220 #x > 220 when gift too close
gift_far=200 #x < 200 when gift too far

def pixyDetectItem():
    x = pixy_object.get_blocks()
    #print 'block: ' + str(x)
    if x[0]==1:
        return 'tree'
    elif x[0]==2:
        if x[1]>=gift_far and x[1]<=gift_near and x[2]>=gift_left and x[2]<=gift_right:
            print 'right in front'
            return 'gift'
        if x[1]<200:
            print 'move forward'
            return 'gift'
        if x[2]<160:
            print 'move left'
            return 'gift'
        if x[2]>180:
            print 'move right'
            return 'gift'
    elif x[0]==0:
        return 'None'
    else:
        return 'other'

def pixyApproach():
    itemFound = pixyDetectItem()
    x=pixy_object.get_blocks()
    if x[0]==1: #tree
    elif x[0]==2: #gift
        while x[2]<=gift_left or x[2]>=gift_right:
            # adjust L/R until gift is in center (slowly)
            if x[2]<=gift_left:
                #move left
                print 'move left'
            elif x[2]>=gift_right: 
                #move right
                print 'move right'
        while x[1]<=gift_far or x[1]>=gift_near:
            if x[1]<=gift_far:
                #move forward
                print 'move forward'
            elif x[1]>=gift_far:
                #move back
                print 'move back'
	return 'pickup'

while True:
    print pixyDetectItem()
    sleep(0.5)
