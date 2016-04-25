#!/usr/bin/env python
from pixy import *
from ctypes import *
import time
# Pixy Python SWIG get blocks example #

print ("Pixy Python SWIG Example -- Get Blocks")
print ("ARE YOU RUNNING AS ROOT??")

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
            # Blocks found #
#            print 'frame %3d:' % (self.frame)
            self.frame = self.frame + 1
            for index in range (0, count):
#                print '[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (self.blocks[index].type, self.blocks[index].signature, self.blocks[index].x, self.blocks[index].y, self.blocks[index].width, self.blocks[index].height)
#                sig=self.blocks[index].signature
                return self.blocks[index].signature,self.blocks[index].x,self.blocks[index].y,self.blocks[index].width,self.blocks[index].height
#                if sig==1:
#                    return 1
#                elif sig==2:
#                    return 2
        else:
            #print 'No Blocks Found.'        
            return 0,0,0,0,0
        #return self.blocks

    def get_blocks_and_print(self):
        count = pixy_get_blocks(100, self.blocks)
        if count > 0:
            # Blocks found #
#            print 'frame %3d:' % (self.frame)
            self.frame = self.frame + 1
            for index in range (0, count):
                print '[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (self.blocks[index].type, self.blocks[index].signature, self.blocks[index].x, self.blocks[index].y, self.blocks[index].width, self.blocks[index].height)
#                sig=self.blocks[index].signature
                return self.blocks[index].signature,self.blocks[index].x,self.blocks[index].y,self.blocks[index].width,self.blocks[index].height
#                if sig==1:
#                    return 1
#                elif sig==2:
#                    return 2
        else:
            #print 'No Blocks Found.'        
            return 0,0,0,0,0
        #return self.blocks    

if __name__=="__main__":
    x=easy_pixy()
    while 1:
        x.get_blocks()
        time.sleep(0.5)
