import Motor
import Claw
import Encoders
import pid_control
from Adafruit_ADS1x15 import ADS1x15
from time import sleep
import time 

COUNTS_FORWARD = 200
COUNTS_TURN_MAX_L = 140
COUNTS_TURN_MIN_L = 140
COUNTS_TURN_MAX_R = 140
COUNTS_TURN_MIN_R = 140

PWM_TURN_R= 900
PWM_TURN_L = 800
PWM_DEFAULT = 800
PWM_MAX = 900
PWM_MIN = 700

IR_GAIN = 4096
IR_SPS = 500
IR_LEFT = 1
IR_MIDDLE = 2
IR_RIGHT = 3

P_GAIN = 6
I_GAIN = 0.02
D_GAIN = 0.1

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

	def turnRight(self):
		print '######## TURNING RIGHT ########'

		self.leftMotor.forward()
		self.rightMotor.backward()

		self.turn_robot(COUNTS_TURN_MAX_R, COUNTS_TURN_MIN_R, PWM_TURN_R)

	def turnAround(self):
		print '######## TURNING AROUND ########'

		self.turnLeft()
		self.turnLeft()

	def move_robot(self, previous_decision):

		#init_Rcount = self.encoders.get_right_wheel_count()
		#init_Lcount = self.encoders.get_left_wheel_count()

		#print "init_Rcount: ", init_Rcount
		#print "init_Lcount: ", init_Lcount

		#left_error = left_goal
		#right_error = right_goal
		ir_data = self.getIrSensorData()
		print (ir_data)
		left_ir = ir_data[0]
		right_ir = ir_data[2]
		middle_ir = ir_data[1]
		print "****DECISION*****", previous_decision
		if previous_decision != -1:
		
			while ir_data[previous_decision] > 15:
				ir_data = self.getIrSensorData()
				print (ir_data)
                		self.leftMotor.setSpeed(PWM_DEFAULT)
                		self.rightMotor.setSpeed(PWM_DEFAULT)
			self.stop()
		

		loop_check = 0
		self.rightPid.reset()
		self.leftPid.reset()

		while (left_ir < 15 ) and (right_ir < 15):
			#R_pwm_speed = self.rightPid.get_pwm(right_error)
			#L_pwm_speed = self.leftPid.get_pwm(left_error)
			
			ir_data = self.getIrSensorData()
                	print (ir_data)
                	left_ir = ir_data[0]

                	right_ir = ir_data[2]
                	middle_ir = ir_data[1]
			
			if middle_ir < 6:
				break
			R_pwm_speed = PWM_DEFAULT

			L_pwm_speed = PWM_DEFAULT

			if (left_ir < right_ir):
                		L_pwm_speed += (15 - left_ir) * 5
				R_pwm_speed -= (15 - left_ir) * 5
				#print "Print left speed: ", L_pwm_speed
                		#print "TURN TOWARDS RIGHT"
			
            		elif (right_ir < left_ir):
                		R_pwm_speed += (15 - right_ir) * 5
				L_pwm_speed -= (15 - right_ir) * 5
				#print "TURN TOWARDS LEFT"
             
			if R_pwm_speed > PWM_MAX:
				R_pwm_speed = PWM_MAX
			elif R_pwm_speed < PWM_MIN:
				R_pwm_speed = PWM_MIN
			if L_pwm_speed > PWM_MAX:
				L_pwm_speed = PWM_MAX
			elif L_pwm_speed < PWM_MIN:
				L_pwm_speed = PWM_MIN

			#print "Right PWM: ", int(R_pwm_speed)
			#print "Left PWM: ",int( L_pwm_speed)

			self.leftMotor.setSpeed(int(L_pwm_speed))
			self.rightMotor.setSpeed(int(R_pwm_speed))

	       		sleep(0.005)

	       	self.stop()
		#sleep(.005)

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
	
	def step_forward(self):
		ir_data = self.getIrSensorData()
                print "############### IR DATA ############"
                print ir_data[1]

               	if ir_data[1] < 5:
			print "CHECK IF TOO CLOSE TO WALL"
			self.leftMotor.backward()
			self.rightMotor.backward()
			sleep(.5)
			self.stop()

		self.leftMotor.forward()
                self.rightMotor.forward()
		self.leftMotor.setSpeed(PWM_DEFAULT)
		self.rightMotor.setSpeed(PWM_DEFAULT)
		print "****** STEPPING FORWARD *********"
		tic = time.time()
		toc = tic
		while toc - tic < 2.5:
			ir_data = self.getIrSensorData()
                	if ir_data[1] < 6:
				break
			toc = time.time()
           	self.stop()		
	
	def stop(self):

		self.leftMotor.stop()
		self.rightMotor.stop()

	def getIrSensorData(self):

		distanceL = []
		distanceM = []
		distanceR = []

		for i in xrange(20):
			voltsL = self.irSensors.readADCSingleEnded(IR_LEFT, IR_GAIN, IR_SPS)/1000
			distanceL.append(self.irDist(voltsL))

			voltsM = self.irSensors.readADCSingleEnded(IR_MIDDLE, IR_GAIN, IR_SPS)/1000
			distanceM.append(self.irDist(voltsM))

			voltsR = self.irSensors.readADCSingleEnded(IR_RIGHT, IR_GAIN, IR_SPS)/1000
			distanceR.append(self.irDist(voltsR))

			sleep(.005)

		finalDistL = sum(distanceL)/len(distanceL)
		finalDistM = sum(distanceM)/len(distanceM)
		finalDistR = sum(distanceR)/len(distanceR)    
	   
		return [finalDistL, finalDistM, finalDistR] 

	''' TODO: Calibrate for each sensor '''
	def irDist(self, volts):
		return 11.721 * volts**(-0.972)

	def pickupGift(self):
		self.claw.pickupGift()

	def dropGift(self):
		self.claw.dropGift()
