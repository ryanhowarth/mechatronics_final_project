#!/usr/bin/python
from pixy import easy_pixy_test
from time import sleep

pixy_object = easy_pixy.easy_pixy()

def pixyDetectItem():
    x = pixy_object.get_blocks()
    if x==1:
        return 'tree'
    elif x==2:
        return 'gift'
    else:
        return ''

while True:
    print pixyDetectItem()
    sleep(0.5)
