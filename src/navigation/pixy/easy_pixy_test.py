#!/usr/bin/env python
from pixy import *
from ctypes import *
import time
# Pixy Python SWIG get blocks example #

class easy_pixy():

    class Blocks (Structure):
      _fields_ = [ ("type", c_uint),
                   ("signature", c_uint),
                   ("x", c_uint),
                   ("y", c_uint),
                   ("width", c_uint),
                   ("height", c_uint),
                   ("angle", c_uint) ]
    blocks = BlockArray(100)
    frame = 0

    def __init__(self):
        pixy_init()
        print "pixy was init"        

    def get_blocks(self):
        count = pixy_get_blocks(100, self.blocks)
        if count > 0:
            self.frame = self.frame + 1
            for index in range (0, count):
		if self.blocks[index].signature==2:
                    return self.blocks[index].signature,self.blocks[index].x,self.blocks[index].y,self.blocks[index].width,self.blocks[index].height
	    else:
		return self.blocks[index].signature,self.blocks[index].x,self.blocks[index].y,self.blocks[index].width,self.blocks[index].height
        else:
            #print 'No Blocks Found.'
            return 0,0,0,0,0

if __name__=="__main__":
    x=easy_pixy()
    while 1:
        print x.get_blocks()
        time.sleep(0.5)
