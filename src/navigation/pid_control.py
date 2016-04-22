#!/usr/bin/env python
import time
import pigpio
import rotary_encoder


class easy_PID():

    #Controller Constants
    p_gain = 0
    i_gain = 0
    d_gain = 0
    prev_error = 0
    accumulator = 0  #sum of errors

    def __init__(self, p_gain, i_gain, d_gain):
        self.p_gain = p_gain
        self.i_gain = i_gain
        self.d_gain = d_gain

    def reset(self):
        self.accumulator = 0
    def get_pwm(self, error):
        PID = self.p_gain*error

        self.accumulator += error
        PID += self.i_gain*self.accumulator

        PID += self.d_gain*(error - self.prev_error)
        self.prev_error = error
        if (PID > 125):
            PID = 125
        if (PID < 0):
            PID = 0
        return int(round(PID))
    

if __name__ == "__main__":
    x = easy_PID(100, 10, 50)
    y = [10, 9, 8, 7, 6, 5, 4, 3.0, 2.0, 1.3]
    i = 0
    while i <  len(y):
        print ("PWM: ", x.get_pwm(y[i]))
        time.sleep(.25)
        i += 1
