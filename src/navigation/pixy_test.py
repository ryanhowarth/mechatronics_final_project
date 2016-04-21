#!/usr/bin/python
from pixy import easy_pixy
from time import sleep

pixy_object = easy_pixy.easy_pixy()

def pixyDetectItem():
    x = pixy_object.get_blocks()
    print 'block: ' + str(x)
    if x==1:
        return 'tree'
    elif x==2:
        return 'gift'
    else:
        return ''

while True:
    print pixyDetectItem()
    sleep(1)
