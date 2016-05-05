import Motor
import Claw
import Encoders
import pid_control
from Adafruit_ADS1x15 import ADS1x15
from time import sleep
import time 
from pixy import easy_pixy_test
import IrSensor

#Threading stuff for spinning off irsensor thread
import Queue
from threading import Thread


#logging modules
import logging, coloredlogs


#Array Indices that IrSensors are in.
IR_LEFT = 0
IR_MIDDLE = 1
IR_RIGHT = 2
NUM_IR_SAMPLES = 10

PWM_MAX = 900
PWM_MIN = 800

#Counts for stuff
TURN_RADIUS_CORR_COUNT = 180
COUNT_TURN_LEFT = 155
COUNT_TURN_RIGHT = 155
TURNING_STOPPING_SPEED = 600

#Default pwm values to go straight
PWM_NOMINAL_LEFT = 814
PWM_NOMINAL_RIGHT = 800
#at higher speed (Not used right now)
PWM_FAST_LEFT = 925
PWM_FAST_RIGHT = 900

BACKWARD_TIME = 0.5
#Wall correction gains
P_GAIN = 6
I_GAIN = 1
D_GAIN = 6
PREVIOUS_CORRECTION_VALUE = 0 

#Wall Thresholds
MAX_WALL_THRESH = 17
#MIN_WALL_THRESH = 10
MIN_FRONT_WALL_THRESH = 7
IDEAL_DIST_FROM_WALL = 11.5

#Control Parameters
loop_freq = 20


#Objects
#irSensors = []
logger = []

#DELIVERY PARAMETERS
#Motor turning PWM
ADJUST_MAX = 25
ADJUST_MIN = 25
PWM_ADJUST = 860
ADJUST_LR_TIME=.02
ADJUST_F_TIME=.1
ADJUST_B_TIME=.10
#Pixy
# 0 is to the left of the robot
# 160 is to the right
SIG_TREE=1
SIG_GIFT=2
GIFT_RIGHT=105
GIFT_LEFT=115
TREE_RIGHT=100
TREE_LEFT=120
#IR
GIFT_FAR=13
GIFT_NEAR=9
TREE_FAR=11
TREE_NEAR=9

class robot():

	def __init__(self, leftMotorOutA, leftMotorOutB, leftPwm, rightMotorOutA, rightMotorOutB, rightPwm, liftServoPin, pinchServoPin):
		#Set up colorized logger
		self.logger = logging.getLogger('maze_run')
		coloredlogs.install(level='DEBUG')
		

		#Create objects related to robot
		self.logger.info('create robot')
		self.leftMotor = Motor.motor(leftMotorOutA, leftMotorOutB, leftPwm)
		self.rightMotor = Motor.motor(rightMotorOutA, rightMotorOutB, rightPwm)
		self.claw = Claw.claw(liftServoPin, pinchServoPin)
		self.irSensors = IrSensor.irSensor()
		self.encoders = Encoders.easy_encoders()
		self.leftPid = pid_control.easy_PID(P_GAIN, I_GAIN, D_GAIN)
		self.rightPid = pid_control.easy_PID(P_GAIN, I_GAIN, D_GAIN)
      		self.pixyObj = easy_pixy_test.easy_pixy()
		self.PREVIOUS_CORRECTION_VALUE = 0
	
		self.pickedup = False

	def __del__(self):
		self.logger.info('shut down robot')

		del self.leftMotor
		del self.rightMotor
		del self.claw
		del self.irSensors
		del self.encoders
		del self.leftPid
		del self.rightPid

#############################################################################
################# Top Level Functions Used by Navigation ####################
#############################################################################	
	#moves robot forward and the right wall disapears.
	# does on the fly positional correction based on location of right wall.
	#@profile
	def moveForwardUntilNoWall(self):
		
		irData = self.getIrSensorData()
		#self.test_thread()
		while irData[IR_RIGHT] < MAX_WALL_THRESH:
			start_time = time.time() #Must always be first line in fuction.
			irData = self.getIrSensorData()
			self.logger.debug("MOVE FORWARD irData: " + str(irData))
			#self.test_thread()
			if not self.checkFrontWall(irData):
				return False
			
			
			self.sleepToEndLoop(start_time)
			self.moveForward()
			self.correctToRightWall(irData)
		self.stop()
		return True
	
	#moves forward trying to find right wall.
	#does not do positional correction. 
	#TODO:
	#could use left wall to do corrections at some point in futur
	def moveForwardToFindRightWall(self):
		irData = self.getIrSensorData()
		
		while irData[IR_RIGHT] > MAX_WALL_THRESH:
			start_time = time.time() #Must always be first line in fuction.
			
			irData = self.getIrSensorData()
			
			if not self.checkFrontWall(irData):
				return False
			
			
			self.sleepToEndLoop(start_time)
			self.moveForward()
			#self.correctToLeftWall(irData)
		self.stop()
		return 2

	#Moves foreward a specified amount to so a turn does get blocked by a wall
	def moveForwardToClearTurnRadius(self):
		irData = self.getIrSensorData()
		init_Rcount = self.encoders.get_right_wheel_count()
                init_Lcount = self.encoders.get_left_wheel_count()
	 	Rcount = 0
		Lcount = 0
		while Rcount < TURN_RADIUS_CORR_COUNT and Lcount < TURN_RADIUS_CORR_COUNT:
			start_time = time.time()
			irData = self.getIrSensorData()
			self.moveForward()
			#Get encoder data
			Rcount = self.encoders.get_right_wheel_count() - init_Rcount
			Lcount = self.encoders.get_left_wheel_count() - init_Lcount
			#Check Front Wall
			if not self.checkFrontWall(irData):
				return False
			
			self.sleepToEndLoop(start_time)
			self.correctToLeftWall(irData)
		self.stop()

	def moveBackward(self):
		self.leftMotor.backward()
		self.rightMotor.backward()

		self.leftMotor.setSpeed(PWM_NOMINAL_LEFT)
		self.rightMotor.setSpeed(PWM_NOMINAL_RIGHT)
		
		sleep(BACKWARD_TIME)

		self.stop()
	
	def turnLeft(self):
		#Turn the motor a specified number of counts
		self.leftMotor.backward()
		self.rightMotor.forward()
		self.turn_robot2(COUNT_TURN_LEFT)
		
		#Stop the turn by driving the motor the other way briefly.
		self.leftMotor.forward()
		self.rightMotor.backward()
		self.leftMotor.setSpeed(TURNING_STOPPING_SPEED)
                self.rightMotor.setSpeed(TURNING_STOPPING_SPEED)
		sleep(0.1)
		self.stop()	
		
	
	def turnRight(self):
		#Turn the motor a specified number of counts
		self.leftMotor.forward()
		self.rightMotor.backward()
		self.turn_robot2(COUNT_TURN_RIGHT)
		
		#Stop the turn by driving the motor the other way briefly.
		self.leftMotor.backward()
		self.rightMotor.forward()
		self.leftMotor.setSpeed(TURNING_STOPPING_SPEED)
                self.rightMotor.setSpeed(TURNING_STOPPING_SPEED)
		sleep(0.1)
		self.stop()	
			
#############################################################################
############### Sub Functions Called by Top Level Functions #################
#############################################################################	
	#Called by turnLeft and turnRight
	#turns the robot a specified number of counts either way.
	def turn_robot2(self, num_of_counts):
		init_Rcount = self.encoders.get_right_wheel_count()
                init_Lcount = self.encoders.get_left_wheel_count()
		Lcount = 0
		Rcount = 0
		turningoffset = 75 #higher speed to turn more accurately
                while Lcount < num_of_counts and Rcount < num_of_counts:
                        #Set speed
			self.leftMotor.setSpeed(PWM_NOMINAL_LEFT + turningoffset)
                        self.rightMotor.setSpeed(PWM_NOMINAL_RIGHT + turningoffset)
                        sleep(0.005)
			
			#Get encoder data
                        Lcount = abs(self.encoders.get_right_wheel_count() - init_Rcount)
                        Rcount = abs(self.encoders.get_left_wheel_count() - init_Lcount)

		self.stop()	
	
	#checks to see how far robot is from right wall.
	#if it is within +/- 2 it does nothing, otherwise calls correction functions
	def correctToRightWall(self, irData):
		if (irData[IR_RIGHT] > MAX_WALL_THRESH):
			#self.logger.warn("RIGHT WALL TOO FAR AWAY. Consider using LEFT")
			self.correctToLeftWall(irData)
			
		if irData[IR_RIGHT] > IDEAL_DIST_FROM_WALL - 1 and irData[IR_RIGHT] <IDEAL_DIST_FROM_WALL + 1:
			return 
		elif irData[IR_RIGHT] < IDEAL_DIST_FROM_WALL:
			self.correctLeft(IDEAL_DIST_FROM_WALL - irData[IR_RIGHT])
		else: 	
			self.correctRight(irData[IR_RIGHT] - IDEAL_DIST_FROM_WALL)

	#checks to see how far robot is from right wall.
	#if it is within +/- 2 it does nothing, otherwise calls correction functions
	def correctToLeftWall(self, irData):
		if (irData[IR_LEFT] > MAX_WALL_THRESH):
			self.logger.warn("LEFT WALL TOO FAR AWAY.")
			
		if irData[IR_LEFT] > IDEAL_DIST_FROM_WALL - 2 and irData[IR_LEFT] <IDEAL_DIST_FROM_WALL + 2:
			return 
		elif irData[IR_LEFT] < IDEAL_DIST_FROM_WALL:
			self.correctRight((IDEAL_DIST_FROM_WALL - irData[IR_LEFT]) / 2)
		else: 	
			self.correctLeft((irData[IR_LEFT] - IDEAL_DIST_FROM_WALL) / 2)
	

	#slight correction to the left.
	#Calulates error exponetially
	def correctLeft(self, error):
		#Calculate correction differently based on distance away
		correction = error * P_GAIN
		correction += D_GAIN * (error - self.PREVIOUS_CORRECTION_VALUE)
		self.PREVIOUS_CORRECTION_VALUE = error
		self.logger.warn("CORRECTION LEFT: " + str(correction))
		
		#Send commands to motors
		self.leftMotor.setSpeed(int(PWM_NOMINAL_LEFT - correction))
		self.rightMotor.setSpeed(int(PWM_NOMINAL_RIGHT + correction))
		#self.logger.debug("CORRECT LEFT PWM_VALS: " +  str([PWM_NOMINAL_LEFT - correction, PWM_NOMINAL_RIGHT+ correction]))
	#slight correction to the right
	#Calulates error exponetially
	def correctRight(self, error):
		#Calculate the PID constants
		correction = error * P_GAIN
		correction += D_GAIN * (error - self.PREVIOUS_CORRECTION_VALUE)
		self.PREVIOUS_CORRECTION_VALUE = error
		self.logger.warn("CORRECTION RIGHT: " + str(correction))
		#Send to Motor
		self.leftMotor.setSpeed(int(PWM_NOMINAL_LEFT + correction))
		self.rightMotor.setSpeed(int(PWM_NOMINAL_RIGHT - correction))
		#self.logger.debug("CORRECT RIGHT PWM_VALS: " + str([PWM_NOMINAL_LEFT + correction, PWM_NOMINAL_RIGHT- correction]))
	

	#Checks if robot is going to hit front wall.
	#Stops the robot in this case.
	def checkFrontWall(self, irData):
		if irData[IR_MIDDLE] < MIN_FRONT_WALL_THRESH:
			self.stop()
			self.logger.debug("STOPPED BECAUSE WALL TOO CLOSE")
			return False
		else:
			return True
		
	#This function sleeps at the end of loop in order to keep a desired control freqency
	#This is specified in the global variable 'loop_freq'
	#If the freqency is set to high and the code can't keep up, it prints errors.	
	def sleepToEndLoop(self, start_time):
		loop_run_time = time.time() - start_time
		time_in_one_loop_cycle = 1.0 / loop_freq
		sleep_time = time_in_one_loop_cycle - loop_run_time
		if sleep_time < 0:
			self.logger.error("YOUR LOOP FREQUENCY IS SET T00 HIGH.")
			self.logger.error("actual running frequency is lower than specified.")
		else:
			sleep(sleep_time)

	#Moves robot foreward at nominial speed indefinitely.
	#TODO
	#Put speed argument in at some point
	def moveForward(self): 

		self.leftMotor.forward()
		self.rightMotor.forward()
		self.leftMotor.setSpeed(PWM_NOMINAL_LEFT)
		self.rightMotor.setSpeed(PWM_NOMINAL_RIGHT)
		#self.move_robot(previous_decision)

	def stop(self):

		self.leftMotor.stop()
		self.rightMotor.stop()
	

	def getIrSensorData(self):
		return self.irSensors.getIrSensorData()
		#return self.q.get()

	# ----------------------- DELIVERY MECHANISM ------------------------
	def adjustLeftTowardItem(self):
		print '####### ADJUST LEFT #######'
		#self.leftMotor.backward()
		self.rightMotor.forward()
		#self.turn_robot(ADJUST_MAX, ADJUST_MIN, PWM_TURN_L)
		#self.leftMotor.setSpeed(PWM_ADJUST)
                self.rightMotor.setSpeed(PWM_ADJUST)
                sleep(ADJUST_LR_TIME)
                self.stop()


	def adjustRightTowardItem(self):
		print '####### ADJUST RIGHT #######'		
		self.leftMotor.forward()
		#self.rightMotor.backward()
		#self.turn_robot(ADJUST_MIN, ADJUST_MAX, PWM_TURN_R)
		self.leftMotor.setSpeed(PWM_ADJUST)
                #self.rightMotor.setSpeed(PWM_ADJUST)
                sleep(ADJUST_LR_TIME)
                self.stop()


	def adjustForwardTowardItem(self):
		print '####### ADJUST FORWARD #######'
		self.leftMotor.forward()
		self.rightMotor.forward()
		self.leftMotor.setSpeed(PWM_ADJUST)
		self.rightMotor.setSpeed(PWM_ADJUST)
                sleep(ADJUST_F_TIME)
                self.stop()
	
	def adjustBackwardTowardItem(self):
		print '####### ADJUST BACK #######'
		self.leftMotor.backward()
		self.rightMotor.backward()
		self.leftMotor.setSpeed(PWM_ADJUST)
		self.rightMotor.setSpeed(PWM_ADJUST)
                sleep(ADJUST_B_TIME)
                self.stop()

	def pickupGift(self):
		self.claw.pickupGift()

	def dropGift(self):
		self.claw.dropGift()

	def detectItem(self):
		blocks = self.pixyObj.get_blocks()
		signature = blocks[0]
		if signature == SIG_GIFT:
			while not self.pickedup:
				self.pickedup = self.approachGift()
			self.leftMotor.forward()
			self.rightMotor.backward()
			
			self.leftMotor.setSpeed(PWM_NOMINAL_LEFT)
			self.rightMotor.setSpeed(PWM_NOMINAL_RIGHT)
			sleep(0.1)
			self.stop()
		elif signature == SIG_TREE and self.pickedup:
			dropped = False
			while not dropped:
				dropped = self.approachTree()
			return True

		return False

	# Returns true if pickup or dropoff succesful
	def approachTree(self):
		x=self.pixyObj.get_blocks()
		ir_data = self.getIrSensorData()
		while (x[2] <= TREE_RIGHT or x[2] >= TREE_LEFT) or (ir_data[1] >= TREE_FAR or ir_data[1] <= TREE_NEAR):
			print x[2]
			while x[2]<=TREE_RIGHT:
				self.adjustRightTowardItem()
				x=self.pixyObj.get_blocks()
			while x[2]>=TREE_LEFT:
				self.adjustLeftTowardItem()
				x=self.pixyObj.get_blocks()
			if ir_data[1] >= TREE_FAR:
				self.adjustForwardTowardItem()
                                ir_data = self.getIrSensorData()
				print ir_data[1]
			elif ir_data[1] <= TREE_NEAR:
				#print 'Back'
				self.adjustBackwardTowardItem()
				ir_data = self.getIrSensorData()
				print ir_data[1]
			x=self.pixyObj.get_blocks()
			
		sleep(0.2)
		print 'Reached dropoff location'
		self.dropGift()
		return True

	def approachGift(self):
		x = self.pixyObj.get_blocks()
		ir_data = self.getIrSensorData()
		right_dis=False
        	while (x[2]<=GIFT_RIGHT or x[2]>=GIFT_LEFT) or (ir_data[1] >= GIFT_FAR or ir_data[1] <= GIFT_NEAR):
			print 'Gift block ', x[2]
			if ir_data[1]>=GIFT_NEAR and ir_data[1]<=GIFT_FAR:
				right_dis=True
			while x[2]<=GIFT_RIGHT:
				print 'Right'
				self.adjustRightTowardItem()
				x=self.pixyObj.get_blocks()
			#	ir_data = self.getIrSensorData()
			#	print 'd=',ir_data[1]
			while x[2]>=GIFT_LEFT:
				print 'Left'
				self.adjustLeftTowardItem()
				x=self.pixyObj.get_blocks()
			#	ir_data = self.getIrSensorData()
			#	print 'd=',ir_data[1]
			if right_dis:
				break
			if ir_data[1] >= GIFT_FAR:
				print 'Forward'
				self.adjustForwardTowardItem()
				#sleep(0.1)
			#	ir_data = self.getIrSensorData()
			#	print 'd=',ir_data[0]
			elif ir_data[1] <= GIFT_NEAR:
				print 'Back'
				self.adjustBackwardTowardItem()
				#sleep(0.1)
			#	ir_data = self.getIrSensorData()
			#	print 'd=',ir_data[1]
			#sleep(0.2)
			ir_data = self.getIrSensorData()
			print 'd=',ir_data[1]
			'''
			if ir_data[1]>15 and ir_data[1]<30:
				t=(ir_data[1]-15)/5.5
				self.leftMotor.forward()
				self.rightMotor.forward()
				self.leftMotor.setSpeed(PWM_ADJUST)
				self.rightMotor.setSpeed(PWM_ADJUST)
                		sleep(t)
		                self.stop()
			'''
			x=self.pixyObj.get_blocks()
			
		sleep(0.2)
		print 'Reached pickup location'

#		self.rightMotor.backward()
#                self.rightMotor.setSpeed(PWM_ADJUST)
#                sleep(0.01)
#                self.stop()
		
		self.pickupGift()
		'''
		stillThere=self.detectItem()
		if(stillThere=='gift'):
			return False
		'''
		x = self.pixyObj.get_blocks()
		
		return not (x[0] == SIG_GIFT and x[1] > 60)

	


