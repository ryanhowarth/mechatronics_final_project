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
COUNT_TURN_LEFT = 150
COUNT_TURN_RIGHT = 150


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
MIN_FRONT_WALL_THRESH = 5
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
	#moves robot forward and the right wall disapears.
	# does on the fly positional correction based on location of right wall.
	@profile
	def moveForwardUntilNoWall(self):
		
		irData = self.getIrSensorData()

		while irData[IR_RIGHT] < MAX_WALL_THRESH:
			start_time = time.time() #Must always be first line in fuction.
			irData = self.getIrSensorData()
			
			if not self.checkFrontWall(irData):
				return -1
			
			
			self.sleepToEndLoop(start_time)
			self.moveForward()
			self.correctToRightWall(irData)
		self.stop()
		return 2
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
				return -1
			
			
			self.sleepToEndLoop(start_time)
			self.moveForward()
		self.stop()
		return 2

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
			

	def turn_robot2(self):
		init_Rcount = self.encoders.get_right_wheel_count()
                init_Lcount = self.encoders.get_left_wheel_count()
		Lcount = 0
		Rcount = 0

                while Lcount < COUNT_TURN_LEFT and Rcount < COUNT_TURN_RIGHT:
                        
			self.leftMotor.setSpeed(PWM_NOMINAL_LEFT)
                        self.rightMotor.setSpeed(PWM_NOMINAL_RIGHT)

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

	#slight correction to the left
	def correctLeft(self, error):
		correction = int((error * error) * L_GAIN)
		self.leftMotor.setSpeed(PWM_NOMINAL_LEFT - correction)
		self.rightMotor.setSpeed(PWM_NOMINAL_RIGHT + correction)
		print "PWM_VALS: ", [PWM_NOMINAL_LEFT - correction, PWM_NOMINAL_RIGHT+ correction]
	#slight correction to the right
	def correctRight(self, error):
		correction = int((error * error)*R_GAIN)
		self.leftMotor.setSpeed(PWM_NOMINAL_LEFT + correction)
		self.rightMotor.setSpeed(PWM_NOMINAL_RIGHT - correction)
		print "PWM_VALS: ", [PWM_NOMINAL_LEFT + correction, PWM_NOMINAL_RIGHT- correction]
	


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
	def moveForward(self, previous_decision=-1):#remove previous decision and put speed arguent at some point 

		self.leftMotor.forward()
		self.rightMotor.forward()
		self.leftMotor.setSpeed(PWM_NOMINAL_LEFT)
		self.rightMotor.setSpeed(PWM_NOMINAL_RIGHT)
		#self.move_robot(previous_decision)

	def stop(self):

		self.leftMotor.stop()
		self.rightMotor.stop()
	
	def turnLeft(self):
		print '######## TURNING LEFT ########'

		self.leftMotor.backward()
		self.rightMotor.forward()

		self.turn_robot2()
	def turnRight(self):
		print '######## TURNING RIGHT ########'

		self.leftMotor.forward()
		self.rightMotor.backward()

		self.turn_robot2()





	
	def adjustLeft(self):
		print '####### ADJUST LEFT #######'
		self.leftMotor.backward()
		self.rightMotor.forward()

		self.turn_robot(ADJUST_MAX, ADJUST_MIN, PWM_TURN_L)

	def adjustRight(self):
		print '####### ADJUST RIGHT #######'		
		self.leftMotor.forward()
		self.rightMotor.backward()

		self.turn_robot(ADJUST_MIN, ADJUST_MAX, PWM_TURN_R)

	def adjustForward(self):
		print '####### ADJUST FORWARD #######'
		self.leftMotor.forward()
		self.rightMotor.forward()
		self.leftMotor.setSpeed(PWM_ADJUST)
		self.rightMotor.setSpeed(PWM_ADJUST)
                sleep(0.25)
                self.stop()
	
	def adjustBackward(self):
		print '####### ADJUST BACK #######'
		self.leftMotor.backward()
		self.rightMotor.backward()
		self.leftMotor.setSpeed(PWM_ADJUST)
		self.rightMotor.setSpeed(PWM_ADJUST)
                sleep(0.25)
                self.stop()
		

	def turnAround(self):
		print '######## TURNING AROUND ########'

		self.turnLeft()
		self.turnLeft()

	def goStraight(self):
		self.leftMotor.forward()
		self.rightMotor.forward()
		
		self.leftMotor.setSpeed(PWM_DEFAULT)
		self.rightMotor.setSpeed(PWM_DEFAULT)

	def move_robot(self, decision):
		print 'in move_robot'
		ir_data = self.getIrSensorData()
		# Waiting to exit previous intersection
		wallToFollow = decision
		if ir_data[1] < 4:
			self.stop()
		# Stop if too close to front wall
		ir_data = self.getIrSensorData()

		self.leftMotor.forward()
                self.rightMotor.forward()
	
		tic = time.time()
		toc = tic
		while toc - tic < 2.5:
			ir_data = self.followWall(wallToFollow)
			if (ir_data[1] < 8):
				break	
			toc = time.time()
		self.stop()		
	
	def followWall(self, wallToFollow):

		#print 'in followWall'

		ir_data = self.getIrSensorData()
                print ir_data,'following wall. SUP'
		# Case that should rarely (never) happen
               	if ir_data[1] < 4:
                       	return ir_data

              	R_pwm_speed = PWM_DEFAULT
               	L_pwm_speed = PWM_DEFAULT

		# Proportional control of motors
		if ir_data[wallToFollow] < WALL_THRESH:
			magnitude = 14 - ir_data[wallToFollow]
			if wallToFollow == 0:
				print 'following left ', magnitude
				L_pwm_speed += magnitude * GAIN_L
                        	R_pwm_speed -= magnitude * GAIN_R
			elif wallToFollow == 2:
				print 'following right ', magnitude
				R_pwm_speed += magnitude * GAIN_R
				L_pwm_speed -= magnitude * GAIN_L
            		
		# Constrain PWM to constants
               	if R_pwm_speed > PWM_MAX:
                    	R_pwm_speed = PWM_MAX
       		elif R_pwm_speed < PWM_MIN:
                      	R_pwm_speed = PWM_MIN
            	if L_pwm_speed > PWM_MAX:
                       	L_pwm_speed = PWM_MAX
               	elif L_pwm_speed < PWM_MIN:
                     	L_pwm_speed = PWM_MIN

		print 'L: ',L_pwm_speed
		print 'R: ',R_pwm_speed

		# Set motor speeds
             	self.leftMotor.setSpeed(int(L_pwm_speed))
            	self.rightMotor.setSpeed(int(R_pwm_speed))
              	
		return ir_data
	
	def turn_robot(self, left_goal, right_goal, PWM_TURN):
		init_Rcount = self.encoders.get_right_wheel_count()
                init_Lcount = self.encoders.get_left_wheel_count()

                #print "init_Rcount: ", init_Rcount
                #print "init_Lcount: ", init_Lcount

                left_error = left_goal
                right_error = right_goal

                loop_check = 0
                self.rightPid.reset()
                self.leftPid.reset()

                while (left_error > 10) and (right_error > 10):
                        #R_pwm_speed = self.rightPid.get_pwm(right_error)
                        #L_pwm_speed = self.leftPid.get_pwm(left_error)

                        ir_data = self.getIrSensorData()
                        #print "############### IR DATA ############"
                        #print (ir_data)
                        left_ir = ir_data[0]
                        right_ir = ir_data[2]

                        R_pwm_speed = PWM_TURN

                        L_pwm_speed = PWM_TURN
			#print 'right PWM: ', R_pwm_speed
			#print 'left PWM: ', L_pwm_speed
                        self.leftMotor.setSpeed(int(L_pwm_speed))
                        self.rightMotor.setSpeed(int(R_pwm_speed))

                        sleep(0.005)

                        right_count = self.encoders.get_right_wheel_count()
                        #print "right_count: ", right_count
                        left_count = self.encoders.get_left_wheel_count()
                        #print "left_count: ", left_count

                        right_error = right_goal - abs(right_count - init_Rcount)
                        #print "right_error: ", right_error
                        left_error = left_goal - abs(left_count - init_Lcount)
                        #print "left error: ", left_error

                self.stop()

	def getIrSensorData(self):
		return self.irSensors.getIrSensorData()

	
	def pickupGift(self):
		self.claw.pickupGift()

	def dropGift(self):
		self.claw.dropGift()

	def detectItem(self):
		pass
	# Returns true if pickup or dropoff succesful
	def approachTree(self):
		pass
