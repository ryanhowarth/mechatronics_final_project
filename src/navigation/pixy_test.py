#!/usr/bin/python
from pixy import easy_pixy_test
from time import sleep

pixy_object = easy_pixy_test.easy_pixy()

def pixyDetectItem():
    x = pixy_object.get_blocks()
    #print 'block: ' + str(x)
    if x[0]==1:
        return 'tree'
    elif x[0]==2:
        return 'gift'
    elif x[0]==0:
        return 'None'
    else:
        return 'other'

while True:
    print pixyDetectItem()
    sleep(0.5)
