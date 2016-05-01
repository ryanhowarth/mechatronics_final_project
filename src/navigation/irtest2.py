#!/usr/bin/env python


from time import sleep

import IrSensor

ir = IrSensor.irSensor()

while 1:
	print(ir.getIrSensorData())
	sleep(1)
	
