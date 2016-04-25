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


	def turn_robot(left_goal, right_goal):
		ir_data = get_ir_sensor_data(irSensors)
	        print (ir_data)
	        left_ir = ir_data[0]
	        middle_ir = ir_data[1]
	        right_ir = ir_data[2]
	        if middle_ir < 7:
			motorL.backward()
	                motorR.backward()
	                motorL.setSpeed(int(500 ) )
	                motorR.setSpeed(int(500 ) )
	                sleep(.5)
			motorL.stop()
	                motorR.stop()
	                motorL.forward()
	                motorR.forward()

		init_Rcount = x.get_right_wheel_count()
	        init_Lcount = x.get_left_wheel_count()
	        print "init_Rcount: ", init_Rcount
	        print "init_Lcount: ", init_Lcount
	        LEFT_GOAL_COUNT = left_goal
	        RIGHT_GOAL_COUNT = right_goal
	        left_error = LEFT_GOAL_COUNT
	        right_error = RIGHT_GOAL_COUNT
	        loop_check = 0
	        right_PID_Obj.reset()
	        left_PID_Obj.reset()
	        while (left_error > 10) and (right_error > 10):
	                R_pwm_speed = right_PID_Obj.get_pwm(right_error)
	                L_pwm_speed = left_PID_Obj.get_pwm(left_error)
	                
	                if R_pwm_speed > 900:
	                        R_pwm_speed = 900
	                elif R_pwm_speed < 600:
	                        R_pwm_speed = 600
	                if L_pwm_speed > 900:
	                        L_pwm_speed = 900
	                elif L_pwm_speed < 600:
	                        L_pwm_speed = 600



	                print "------------IR DATA-------------"
	                print "---------------"
	                print "Right PWM: ", R_pwm_speed
	                print "Left PWM: ", L_pwm_speed
	                print "---------------"

	                motorL.setSpeed(int( L_pwm_speed ) )
	                motorR.setSpeed(int( R_pwm_speed ) )

	                right_count = x.get_right_wheel_count()
	                print "right_count: ", right_count
	                left_count = x.get_left_wheel_count()
	                print "left_count: ", left_count

	                right_error = RIGHT_GOAL_COUNT - abs(right_count - init_Rcount)
	                print "right_error: ", right_error
	                left_error = LEFT_GOAL_COUNT - abs(left_count - init_Lcount)
	                print "left error: ", left_error

	        motorL.stop()
	        motorR.stop()

	def move_robot(left_goal, right_goal):
		# Turn robot 90 degrees left
		#print "right wheel count: ", x.get_right_wheel_count()
		#print "left wheel count: ", x.get_left_wheel_count()
		#print "------------------" 
		init_Rcount = x.get_right_wheel_count()
		init_Lcount = x.get_left_wheel_count()
		print "init_Rcount: ", init_Rcount
		print "init_Lcount: ", init_Lcount
		LEFT_GOAL_COUNT = left_goal
		RIGHT_GOAL_COUNT = right_goal
		left_error = LEFT_GOAL_COUNT
		right_error = RIGHT_GOAL_COUNT
		loop_check = 0
		right_PID_Obj.reset()
		left_PID_Obj.reset()
		while (left_error > 10) and (right_error > 10):
			#R_pwm_speed = right_PID_Obj.get_pwm(right_error)
			#L_pwm_speed = left_PID_Obj.get_pwm(left_error)
			R_pwm_speed  = 600
			L_pwm_speed  = 600		
			print "############### IR DATA ############"
			ir_data = get_ir_sensor_data(irSensors)
			print (ir_data)
			left_ir = ir_data[0]
			middle_ir = ir_data[1]
			right_ir = ir_data[2]
			if middle_ir < 7:
				motorL.backward()
				motorR.backward()
				motorL.setSpeed(int( L_pwm_speed ) )
	                	motorR.setSpeed(int( R_pwm_speed ) )
				sleep(1)
				motorL.stop()
				motorR.stop()
				motorL.forward()
				motorR.forward()
				LEFT_GOAL_COUNT -= 30
				RIGHT_GOAL_COUNT -= 30
			if (left_ir < 20):
				if (left_ir > 7) and (left_ir < 8):
					R_pwm_speed = R_pwm_speed - left_ir/5
					print "TOWARDS RIGHT"
				elif (left_ir >8) and (left_ir <14):
					R_pwm_speed =  R_pwm_speed +left_ir/5
					print "TOWARDS LEFT"
				else:
					R_pwm_speed = 100
					L_pwm_speed = 100
			elif (right_ir < 20):
				if (right_ir > 7) and (right_ir < 8):
					L_pwm_speed = L_pwm_speed - right_ir/5
					print "TOWARDS LEFT"
				elif (right_ir > 8) and (right_ir < 14):
					L_pwm_speed = L_pwm_speed + right_ir/5
				else:
					R_pwm_speed = 100
					L_pwm_speed = 100

	        	if R_pwm_speed > 700:
	        		R_pwm_speed = 700
	        	elif R_pwm_speed < 500:
				R_pwm_speed = 500
			if L_pwm_speed > 700:
				L_pwm_speed = 700
			elif L_pwm_speed < 500:
				L_pwm_speed = 500



	        	print "------------IR DATA-------------"
	        	print "---------------"
	        	print "Right PWM: ", R_pwm_speed
	        	print "Left PWM: ", L_pwm_speed
	        	print "---------------"

	        	motorL.setSpeed(int( L_pwm_speed ) )
	        	motorR.setSpeed(int( R_pwm_speed ) ) 
	        	#wp.pwmWrite(PWM_R, R_pwm_speed)
	        	#wp.pwmWrite(PWM_L, L_pwm_spe
	        	sleep(.005)

			right_count = x.get_right_wheel_count()
			print "right_count: ", right_count
			left_count = x.get_left_wheel_count()
			print "left_count: ", left_count
			
			right_error = RIGHT_GOAL_COUNT - abs(right_count - init_Rcount)
			print "right_error: ", right_error
			left_error = LEFT_GOAL_COUNT - abs(left_count - init_Lcount)
			print "left error: ", left_error

		motorL.stop()
		motorR.stop()
		sleep(0)
		#wp.pwmWrite(PWM_R, 0)
		#wp.pwmWrite(PWM_L, 0)




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