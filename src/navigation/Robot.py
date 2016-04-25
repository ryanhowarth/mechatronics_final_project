import Motor
import Claw
import Encoders
import pid_control
from Adafruit_ADS1x15 import ADS1x15

COUNTS_FORWARD = 1000
COUNTS_TURN_MAX = 220
COUNTS_TURN_MIN = 196

PWM_DEFAULT = 100
PWM_MAX = 250
PWM_MIN = 50
PWM_INCREMENT = 5

IR_GAIN = 4096
IR_SPS = 250
IR_LEFT = 0
IR_MIDDLE = 1
IR_RIGHT = 2

P_GAIN = 0.75
I_GAIN = 0.02
D_GAIN = 0.1

class robot():

	def __init__(self, leftMotorOutA, leftMotorOutB, leftPwm, rightMotorOutA, rightMotorOutB, rightPwm, liftServoPin, pinchServoPin):
		print 'create robot'

		self.leftMotor = Motor.motor(leftMotorOutA, leftMotorOutB, leftPwm)
		self.rightMotor = Motor.motor(rightMotorOutA, rightMotorOutB, rightPwm)

		self.claw = Claw.claw(self, liftServoPin, pinchServoPin)

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


	def moveForward(self):
		print '######## MOVING FORWARD ########'

		self.leftMotor.forward()
		self.rightMotor.forward()

		self.move_robot(COUNTS_FORWARD, COUNTS_FORWARD)

	def turnLeft(self):
		print '######## TURNING LEFT ########'

		self.leftMotor.backward()
		self.rightMotor.forward()

		self.move_robot(COUNTS_TURN_MAX, COUNTS_TURN_MIN)

	def turnRight(self):
		print '######## TURNING RIGHT ########'

		self.leftMotor.forward()
		self.rightMotor.backward()

		self.move_robot(COUNTS_TURN_MIN, COUNTS_TURN_MAX)

	def turnAround(self):
		print '######## TURNING AROUND ########'

		self.turnLeft()
		self.turnLeft()

	def move_robot(left_goal, right_goal):

		init_Rcount = self.encoders.get_right_wheel_count()
		init_Lcount = self.encoders.get_left_wheel_count()

		#print "init_Rcount: ", init_Rcount
		#print "init_Lcount: ", init_Lcount

		left_error = left_goal
		right_error = right_goal

		loop_check = 0
		self.rightPid.reset()
		self.leftPid.reset()
		R_pwm_speed = PWM_DEFAULT
		L_pwm_speed = PWM_DEFAULT

		while (left_error > 10) and (right_error > 10):
			#R_pwm_speed = self.rightPid.get_pwm(right_error)
			#L_pwm_speed = self.leftPid.get_pwm(left_error)
			
			ir_data = self.getIrSensorData()			
			print "############### IR DATA ############"
			print (ir_data)
			left_ir = ir_data[0]
			right_ir = ir_data[2]

			if (left_ir < 20):
				if (left_ir > 8):
					R_pwm_speed += PWM_INCREMENT
				elif(left_ir > 2 and left_ir < 5):
					L_pwm_speed += PWM_INCREMENT
				else:
					R_pwm_speed = PWM_DEFAULT
					L_pwm_speed = PWM_DEFAULT
			elif (right_ir < 20):
				if (right_ir > 8):
					L_pwm_speed += PWM_INCREMENT
				elif (right_ir > 2 and right_ir < 5):
					R_pwm_speed += PWM_INCREMENT
				else:
					R_pwm_speed = PWM_DEFAULT
					L_pwm_speed = PWM_DEFAULT

			if R_pwm_speed > PWM_MAX:
				R_pwm_speed = PWM_MAX
			elif R_pwm_speed < PWM_MIN:
				R_pwm_speed = PWM_MIN
			if L_pwm_speed > PWM_MAX:
				L_pwm_speed = PWM_MAX
			elif L_pwm_speed < PWM_MIN:
				L_pwm_speed = PWM_MIN

			print "Right PWM: ", R_pwm_speed
			print "Left PWM: ", L_pwm_speed

			self.leftMotor.setSpeed(L_pwm_speed)
			self.rightMotor.setSpeed(R_pwm_speed)

	       	sleep(0.25)

			right_count = self.encoders.get_right_wheel_count()
	        print "right_count: ", right_count
	        left_count = self.encoders.get_left_wheel_count()
	        print "left_count: ", left_count

	       	right_error = right_goal - abs(right_count - init_Rcount)
	       	print "right_error: ", right_error
	       	left_error = left_goal - abs(left_count - init_Lcount)
	       	print "left error: ", left_error

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
			distanceL.append(irDist(voltsL))

			voltsM = self.irSensors.readADCSingleEnded(IR_MIDDLE, IR_GAIN, IR_SPS)/1000
			distanceM.append(irDist(voltsM))

			voltsR = self.irSensors.readADCSingleEnded(IR_RIGHT, IR_GAIN, IR_SPS)/1000
			distanceR.append(irDist(voltsR))

			sleep(.005)

		finalDistL = sum(distanceL)/len(distanceL)
		finalDistM = sum(distanceM)/len(distanceM)
		finalDistR = sum(distanceR)/len(distanceR)    
	   
		return [finalDistL, finalDistM, finalDistR] 

	''' TODO: Calibrate for each sensor '''
	def irDist(volts):
		return 11.721 * volts**(-0.972)

	def pickupGift(self):
		self.claw.pickupGift()

	def dropGift(self):
		self.claw.dropGift()