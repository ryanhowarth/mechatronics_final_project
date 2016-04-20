#!/usr/bin/python

from time import sleep 
from pixy import easy_pixy


#Pixy 
pixy_object = easy_pixy.easy_pixy()
while 1:
    blocks = pixy_object.get_blocks()
    if (blocks != -1):
        print blocks[0].signature
    sleep(1)


