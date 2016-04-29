import Motor
import Claw
import Encoders
import pid_control
from Adafruit_ADS1x15 import ADS1x15
from time import sleep
import time 
from pixy import easy_pixy_test

COUNTS_FORWARD = 200
COUNTS_TURN_MAX_L = 150
COUNTS_TURN_MIN_L = 150
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

PWM_TURN_R= 800
PWM_TURN_L = 800
PWM_DEFAULT = 810
PWM_MAX = 850
PWM_MIN = 770
PWM_ADJUST = 850

IR_GAIN = 4096
IR_SPS = 500
IR_LEFT = 1
IR_MIDDLE = 2
IR_RIGHT = 3

P_GAIN = 6
I_GAIN = 0.02
D_GAIN = 0.1

SIG_GIFT = 2
SIG_TREE = 1

GAIN_L = 5
GAIN_R = 5

WALL_THRESH = 20

class robot():

	def __init__(self, leftMotorOutA, leftMotorOutB, leftPwm, rightMotorOutA, rightMotorOutB, rightPwm, liftServoPin, pinchServoPin):
		print 'create robot'

		self.leftMotor = Motor.motor(leftMotorOutA, leftMotorOutB, leftPwm)
		self.rightMotor = Motor.motor(rightMotorOutA, rightMotorOutB, rightPwm)

		self.claw = Claw.claw(liftServoPin, pinchServoPin)

		self.irSensors = ADS1x15(ic=0x00)

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


	def moveForward(self, previous_decision):
		print '######## MOVING FORWARD ########'

		self.leftMotor.forward()
		self.rightMotor.forward()

		self.move_robot(previous_decision)

	def turnLeft(self):
		print '######## TURNING LEFT ########'

		self.leftMotor.backward()
		self.rightMotor.forward()

		self.turn_robot(COUNTS_TURN_MAX_L, COUNTS_TURN_MIN_L, PWM_TURN_L)
	
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
		
	def turnRight(self):
		print '######## TURNING RIGHT ########'

		self.leftMotor.forward()
		self.rightMotor.backward()

		self.turn_robot(COUNTS_TURN_MAX_R, COUNTS_TURN_MIN_R, PWM_TURN_R)

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
		while ir_data[decision] > WALL_THRESH:
			# Follow opposite wall if it exists
			if ir_data[(decision + 2) % 4] < WALL_THRESH:
				self.followWall( (decision + 2) % 4)
			# Otherwise go straight
			else:
				self.goStraight()
			ir_data = self.getIrSensorData()
		self.stop()

		# While walls exist on both sides, 
		# follow the wall we came from
		while (ir_data[0] < 20) and (ir_data[2] < 20):
			self.followWall(wallToFollow)
			ir_data = self.getIrSensorData()
		
		tic = time.time()
		toc = tic
		while toc - tic < 1:
			ir_data = self.followWall(wallToFollow)
			#if (ir_data[1] < 8):
			#	break	
			toc = time.time()
		
		self.stop()		
		
	def step_forward(self, wallToFollow):		
	
		print 'in step_forward'

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
               	if ir_data[1] < 8:
                       	return ir_data

              	R_pwm_speed = PWM_DEFAULT
               	L_pwm_speed = PWM_DEFAULT

		# Proportional control of motors
		if ir_data[wallToFollow] < WALL_THRESH:
			magnitude = 10 - ir_data[wallToFollow]
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
	def stop(self):

		self.leftMotor.stop()
		self.rightMotor.stop()

	def getIrSensorData(self):

		distanceL = []
		distanceM = []
		distanceR = []

		for i in xrange(5):
			voltsL = self.irSensors.readADCSingleEnded(IR_LEFT, IR_GAIN, IR_SPS)/1000
			distanceL.append(self.irDistLeft(voltsL))

			voltsM = self.irSensors.readADCSingleEnded(IR_MIDDLE, IR_GAIN, IR_SPS)/1000
			distanceM.append(self.irDistMiddle(voltsM))

			voltsR = self.irSensors.readADCSingleEnded(IR_RIGHT, IR_GAIN, IR_SPS)/1000
			distanceR.append(self.irDistRight(voltsR))

			sleep(.005)

		finalDistL = sum(distanceL)/len(distanceL)
		finalDistM = sum(distanceM)/len(distanceM)
		finalDistR = sum(distanceR)/len(distanceR)    
	   
		return [finalDistL, finalDistM, finalDistR] 

	def irDistLeft(self, volts):
		return 10.189 * volts**(-0.969)

	def irDistMiddle(self, volts):
		return 11.714 * volts**(-1.038)

	def irDistRight(self, volts):
		return 9.6902 * volts**(-0.954)

	def pickupGift(self):
		self.claw.pickupGift()

	def dropGift(self):
		self.claw.dropGift()

	def detectItem(self):
		blocks = self.pixyObj.get_blocks()
		signature = blocks[0]
		if signature == SIG_GIFT:
			return 'gift'
		elif signature == SIG_TREE:
			return 'tree'
        	
		return ''

	# Returns true if pickup or dropoff succesful
	def approachTree(self):
		x=self.pixyObj.get_blocks()
		ir_data = self.getIrSensorData()
		while (x[2] <= TREE_RIGHT or x[2] >= TREE_LEFT) or (ir_data[1] >= TREE_FAR or ir_data[1] <= TREE_NEAR):
			while x[2]<=TREE_RIGHT:
				print 'Right'
				print x[2]
				self.adjustRight()
				x=self.pixyObj.get_blocks()
			while x[2]>=TREE_LEFT:
				print 'Left'
				print x[2]
				self.adjustLeft()
				x=self.pixyObj.get_blocks()
			if ir_data[1] >= TREE_FAR:
				print 'Forward'
				self.adjustForward()
                                ir_data = self.getIrSensorData()
				print ir_data[1]
			elif ir_data[1] <= TREE_NEAR:
				print 'Back'
				self.adjustBackward()
				ir_data = self.getIrSensorData()
				print ir_data[1]
			x=self.pixyObj.get_blocks()
			
		sleep(0.5)
		print 'Reached dropoff location'
		self.dropGift()
		return True

	def approachGift(self):
		x = self.pixyObj.get_blocks()
		ir_data = self.getIrSensorData()
        	while (x[2]<=GIFT_RIGHT or x[2]>=GIFT_LEFT) or (ir_data[1] >= GIFT_FAR or ir_data[1] <= GIFT_NEAR):
			while x[2]<=GIFT_RIGHT:
				print 'Right'
				self.adjustRight()
				x=self.pixyObj.get_blocks()
			while x[2]>=GIFT_LEFT:
				print 'Left'
				self.adjustLeft()
				x=self.pixyObj.get_blocks()
			if ir_data[1] >= GIFT_FAR:
				print 'Forward'
				self.adjustForward()
				ir_data = self.getIrSensorData()
			elif ir_data[1] <= GIFT_NEAR:
				print 'Back'
				self.adjustBackward()
				ir_data = self.getIrSensorData()
			x=self.pixyObj.get_blocks()
		
		sleep(0.5)
		print 'Reached pickup location'
		
		self.pickupGift()
		return True
