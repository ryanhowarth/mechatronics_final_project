#!/usr/bin/python
from pixy import easy_pixy_test
from time import sleep

pixy_object = easy_pixy_test.easy_pixy()
gift_left=160 #y < 160 when gift to left (camera is sideways)
gift_right=180 #y > 180 when gift to right
gift_near=220 #x > 220 when gift too close
gift_far=200 #x < 200 when gift too far
tree_left=160 #y < 160 when tree to left (camera is sideways)
tree_right=180 #y > 180 when tree to right
tree_near=220 #x > 220 when tree too close
tree_far=200 #x < 200 when tree too far



def pixyDetectItem():
    x = pixy_object.get_blocks()
    #print 'block: ' + str(x)
    if x[0]==1:
        return 'tree'
    elif x[0]==2:
        return 'gift'
    elif x[0]==0:
        return 'none'
    else:
        return 'other'

def pixyApproach(item):
    x=pixy_object.get_blocks()
    if item=='tree':
        while x[2]<=tree_left or x[2]>=tree_right:
            # adjust L/R until tree is in center (slowly)
            if x[2]<=tree_left:
                #move left
                print 'move left'
            elif x[2]>=tree_right: 
                #move right
                print 'move right'
        while x[1]<=tree_far or x[1]>=tree_near:
            if x[1]<=tree_far:
                #move forward
                print 'move forward'
            elif x[1]>=tree_far:
                #move back
                print 'move back'
        #dropGift()
        return 'drop'
    elif item='gift':
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
        #pickUpGift()
	return 'pickup'

while True:
    print pixyDetectItem()
    print pixyApproach()
    sleep(0.5)
