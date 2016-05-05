#!/usr/bin/python
from pixy import easy_pixy_test
from time import sleep

pixy_object = easy_pixy_test.easy_pixy()

def pixyDetectItem():
    x = pixy_object.get_blocks()
    print 'X coord', x[1]
    #print 'block: ' + str(x)
    if x[0]==1:
        return 'tree'
    elif x[0]==2:
        if x[1]>=200 and x[1]<=220 and x[2]>=160 and x[2]<=180:
            print 'right in front'
        return 'gift'
    elif x[0]==0:
        return 'None'
    else:
        return 'other'

while True:
    print pixyDetectItem()
    sleep(0.5)
