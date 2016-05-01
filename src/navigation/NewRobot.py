import Motor
import Claw
import Encoders
import pid_control
from Adafruit_ADS1x15 import ADS1x15
from time import sleep
import time 
from pixy import easy_pixy_test
import IrSensor
COUNTS_FORWARD = 200
COUNTS_TURN_MAX_L = 160
COUNTS_TURN_MIN_L = 160
COUNTS_TURN_MAX_R = 170
COUNTS_TURN_MIN_R = 170

ADJUST_MAX = 25
ADJUST_MIN = 25

GIFT_RIGHT=90
GIFT_LEFT=110
TREE_RIGHT=100
TREE_LEFT=120
GIFT_FAR=8.4
GIFT_NEAR=7.4
TREE_FAR=9
TREE_NEAR=7

IR_LEFT = 0
IR_MIDDLE = 1
IR_RIGHT = 2

PWM_TURN_R= 800
PWM_TURN_L = 800
PWM_DEFAULT = 810
PWM_MAX = 900
PWM_MIN = 800
PWM_ADJUST = 850


#Counts for stuff
TURN_RADIUS_CORR_COUNT = 125
COUNT_TURN_LEFT = 160
COUNT_TURN_RIGHT = 145


#Default pwm values to go straight
PWM_NOMINAL_LEFT = 832
PWM_NOMINAL_RIGHT = 800
#at higher speed (Not used right now)
PWM_FAST_LEFT = 925
PWM_FAST_RIGHT = 900



P_GAIN = 6
I_GAIN = 0.02
D_GAIN = 0.1

SIG_GIFT = 2
SIG_TREE = 1

#Wall correction gains
L_GAIN = 2
R_GAIN = 2
#Wall Thresholds
MAX_WALL_THRESH = 17
#MIN_WALL_THRESH = 10
MIN_FRONT_WALL_THRESH = 8
IDEAL_DIST_FROM_WALL = 11

#Control Parameters
loop_freq = 5.0


#Objects
#irSensors = []

class robot():

	def __init__(self, leftMotorOutA, leftMotorOutB, leftPwm, rightMotorOutA, rightMotorOutB, rightPwm, liftServoPin, pinchServoPin):
		print 'create robot'

		self.leftMotor = Motor.motor(leftMotorOutA, leftMotorOutB, leftPwm)
		self.rightMotor = Motor.motor(rightMotorOutA, rightMotorOutB, rightPwm)

		self.claw = Claw.claw(liftServoPin, pinchServoPin)

		self.irSensors = IrSensor.irSensor()

		self.encoders = Encoders.easy_encoders()

		self.leftPid = pid_control.easy_PID(P_GAIN, I_GAIN, D_GAIN)
		self.rightPid = pid_control.easy_PID(P_GAIN, I_GAIN, D_GAIN)

      		self.pixyObj = easy_pixy_test.easy_pixy()

	def __del__(self):
		print 'shut down robot'

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
	def moveForwardUntilNoWall(self):
		
		irData = self.getIrSensorData()

		while irData[IR_RIGHT] < MAX_WALL_THRESH:
			start_time = time.time() #Must always be first line in fuction.
			irData = self.getIrSensorData()
			
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
			self.moveForward()
			Rcount = self.encoders.get_right_wheel_count() - init_Rcount
			Lcount = self.encoders.get_left_wheel_count() - init_Lcount
			self.sleepToEndLoop(start_time)
		self.stop()
	
	def turnLeft(self):
		self.leftMotor.backward()
		self.rightMotor.forward()
		self.turn_robot2(COUNT_TURN_LEFT)
	
	def turnRight(self):
		self.leftMotor.forward()
		self.rightMotor.backward()
		self.turn_robot2(COUNT_TURN_RIGHT)
			
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
		turningoffset = 25
                while Lcount < num_of_counts and Rcount < num_of_counts:
                        
			self.leftMotor.setSpeed(PWM_NOMINAL_LEFT + turningoffset)
                        self.rightMotor.setSpeed(PWM_NOMINAL_RIGHT + turningoffset)

                        sleep(0.005)

                        Lcount = abs(self.encoders.get_right_wheel_count() - init_Rcount)
                        Rcount = abs(self.encoders.get_left_wheel_count() - init_Lcount)

		self.stop()	
	
	#checks to see how far robot is from right wall.
	#if it is within +/- 2 it does nothing, otherwise calls correction functions
	def correctToRightWall(self, irData):
		if (irData[IR_RIGHT] > MAX_WALL_THRESH):
			print "RIGHT WALL TOO FAR AWAY. Consider using LEFT"
			
		if irData[IR_RIGHT] > IDEAL_DIST_FROM_WALL - 2 and irData[IR_RIGHT] <IDEAL_DIST_FROM_WALL + 2:
			return 
		elif irData[IR_RIGHT] < IDEAL_DIST_FROM_WALL:
			self.correctLeft(IDEAL_DIST_FROM_WALL - irData[IR_RIGHT])
		else: 	
			self.correctRight(irData[IR_RIGHT] - IDEAL_DIST_FROM_WALL)

	#slight correction to the left.
	#Calulates error exponetially
	def correctLeft(self, error):
		correction = int((error * error) * L_GAIN)
		self.leftMotor.setSpeed(PWM_NOMINAL_LEFT - correction)
		self.rightMotor.setSpeed(PWM_NOMINAL_RIGHT + correction)
		print "PWM_VALS: ", [PWM_NOMINAL_LEFT - correction, PWM_NOMINAL_RIGHT+ correction]
	#slight correction to the right
	#Calulates error exponetially
	def correctRight(self, error):
		correction = int((error * error)*R_GAIN)
		self.leftMotor.setSpeed(PWM_NOMINAL_LEFT + correction)
		self.rightMotor.setSpeed(PWM_NOMINAL_RIGHT - correction)
		print "PWM_VALS: ", [PWM_NOMINAL_LEFT + correction, PWM_NOMINAL_RIGHT- correction]
	

	#Checks if robot is going to hit front wall.
	#Stops the robot in this case.
	def checkFrontWall(self, irData):
		if irData[IR_MIDDLE] < MIN_FRONT_WALL_THRESH:
			self.stop()
			print "STOPPED BECAUSE WALL TOO CLOSE"
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
			print "YOUR LOOP FREQUENCY IS SET T00 HIGH."
			print "actual running frequency is lower than specified."
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

	
