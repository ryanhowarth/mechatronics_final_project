#!/usr/bin/python
import mapping
from Adafruit_ADS1x15 import ADS1x15
import wiringpi as wp
from time import sleep 
from pixy import easy_pixy
import Adafruit_PCA9685
import pigpio
import rotary_encoder
import pid_control
import motor


#encoders 
pos = 1
pos2  = 1

#Pixy 
#pixy_object = easy_pixy.easy_pixy()

# Initialize sensors
irSensors = ADS1x15(ic=0x00)

#pwm
servoControl = Adafruit_PCA9685.PCA9685()

#left motor
PWM_L = 12  #pin 32 
INPUT_1_LEFT = 8 #pin 24
INPUT_2_LEFT = 25 #pin 22

#right motor
PWM_R = 13 #pin 33
INPUT_1_RIGHT = 11 #pin 23 
INPUT_2_RIGHT = 9 #pin 21

motorL = motor.motor(INPUT_1_LEFT, INPUT_2_LEFT, PWM_L)
motorR = motor.motor(INPUT_1_RIGHT, INPUT_2_RIGHT, PWM_R)

time_turn = .15
time_forward = .4
speedL = 100
speedR = 100 

SERVO_LIFT = 0
SERVO_PINCH = 7

LOWER_SERVO = 175
RAISE_SERVO = 400
OPEN_SERVO = 400
CLOSE_SERVO = 260

servoControl.set_pwm(SERVO_LIFT, 0, RAISE_SERVO)
servoControl.set_pwm(SERVO_PINCH, 0, CLOSE_SERVO)

INPUT_MODE = 0
OUTPUT_MODE = 1
PWM_MODE = 2

'''
wp.wiringPiSetupGpio()
#enable PWM_L
wp.pinMode(PWM_L, PWM_MODE)  #set pin to pwm mode
wp.pwmWrite(PWM_L, 0)

#enable PWM_R
wp.pinMode(PWM_R, PWM_MODE)
wp.pwmWrite(PWM_R, 0)

#enable pins motor1 -- Lmotor
wp.pinMode(INPUT_1_LEFT_MOTOR, OUTPUT_MODE)
wp.pinMode(INPUT_2_LEFT_MOTOR, OUTPUT_MODE)

#enable pins motor2 -- Rmotor
wp.pinMode(INPUT_1_RIGHT_MOTOR, OUTPUT_MODE)
wp.pinMode(INPUT_2_RIGHT_MOTOR, OUTPUT_MODE)

wp.pinMode(12, PWM_MODE)
wp.pinMode(13, PWM_MODE)
wp.pwmSetMode(0)
wp.pwmSetClock(400)
wp.pwmSetRange(1024)
wp.pwmWrite(12,0)
wp.pwmWrite(13,0) 
'''


class easy_encoders():

	#encoder pin numbers on pi (broadcom numbering scheme)
	RW_A = 20 #pin = 38
	RW_B = 26 #pin = 37
	LW_A = 19 #pin = 35
	LW_B = 16 #pin =36

	#encoder counts
	rw_count = 0
	lw_count = 0

	pi_gpio_object = []
	decoder_motorR = []
	decoder_motorL = []
	callback_right_wheel = []
	callback_left_wheel = []

	def __init__(self):
		self.pi_gpio_object = pigpio.pi()
		self.decoder_motorR = rotary_encoder.decoder(self.pi_gpio_object, self.RW_A, self.RW_B, self.callback_right_wheel)
		self.decoder_motorL  = rotary_encoder.decoder(self.pi_gpio_object, self.LW_A, self.LW_B, self.callback_left_wheel)

	def __del__(self):
		self.decoder_motorL.cancel()
		self.decoder_motorR.cancel()
		self.pi_gpio_object.stop()

	def callback_right_wheel(self, way):
		self.rw_count += way
		#print("pos={}".format(self.rw_count))

	def callback_left_wheel(self, way):
		self.lw_count += way
		#print("pos={}".format(self.lw_count))

	def get_right_wheel_count(self):
		return self.rw_count

	def get_left_wheel_count(self):
		return self.lw_count

x = easy_encoders()


'''
def forwardLmotor():
	wp.digitalWrite(INPUT_1_LEFT_MOTOR, 0)
	wp.digitalWrite(INPUT_2_LEFT_MOTOR, 1)

def backwardLmotor():
	wp.digitalWrite(INPUT_1_LEFT_MOTOR, 1)
	wp.digitalWrite(INPUT_2_LEFT_MOTOR, 0)

def forwardRmotor():
	wp.digitalWrite(INPUT_1_RIGHT_MOTOR, 0)
	wp.digitalWrite(INPUT_2_RIGHT_MOTOR, 1)

def backwardRmotor():
	wp.digitalWrite(INPUT_1_RIGHT_MOTOR, 1)
	wp.digitalWrite(INPUT_2_RIGHT_MOTOR, 0)
'''

right_PID_Obj = pid_control.easy_PID(.75, .02, .1)
left_PID_Obj = pid_control.easy_PID(.75, .02, .1)

'''
def moveRobotForward():
	# Move robot forward one grid space
	forwardRmotor()
	forwardLmotor()
	print "#########MOVING FORWARD############"
	move_robot(1000, 1000)

'''

def moveRobotForward():
	# Move robot forward one grid space
	motorL.forward()
	motorR.forward()
	print '#########MOVING FORWARD############'
	move_robot(450, 450)

'''
def turnRobotLeft():
	forwardRmotor()
	backwardLmotor()
	print '#######TURNING LEFT############'
	turn_robot(220, 196)
'''

def turnRobotLeft():
	motorL.backward()
	motorR.forward()
	print '#######TURNING LEFT############'
	turn_robot(220, 196)

'''
def turnRobotRight():
	# Turn robot 90 degrees right
	forwardLmotor()
	backwardRmotor()
	print '##########TURNING RIGHT#########'
	turn_robot(196, 220)
'''

def turnRobotRight():
	# Turn robot 90 degrees right
	motorL.forward()
	motorR.backward()
	print '##########TURNING RIGHT#########'
	turn_robot(196, 220)

def stopMotors():
    motorL.stop()
    motorR.stop()

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

def get_ir_sensor_data(irSensors):
	# Check surroundings for available paths
	gain = 4096
	sps = 250
	distanceL=[]
	distanceM = []
	distanceR = []

	for i in xrange(1, 5):
		voltsL = irSensors.readADCSingleEnded(0,gain,sps)/1000
		distanceL.append(irDistLeft(voltsL))
		voltsM = irSensors.readADCSingleEnded(1,gain,sps)/1000
		distanceM.append(irDistFront(voltsM))
		voltsR = irSensors.readADCSingleEnded(2,gain,sps)/1000
		distanceR.append( irDistRight(voltsR))
		sleep(.005)

	final_distanceL = sum(distanceL)/len(distanceL)
	final_distanceM = sum(distanceM)/len(distanceM)
	final_distanceR = sum(distanceR)/len(distanceR)    
   
	ir_list = [final_distanceL, final_distanceM, final_distanceR] 
	return ir_list 


def turnRobotAround():
	# Turn robot 180 degrees when deadend is found
	turnRobotLeft()
	turnRobotLeft()
	print 'turn around'

def update_intersection(irSensors):
	# Check surroundings for available paths
	gain = 4096
	sps = 250
	distanceL=[]
	distanceM = []
	distanceR = []

	for i in xrange(1, 10):
		voltsL = irSensors.readADCSingleEnded(0,gain,sps)/1000
		distanceL.append(irDistLeft(voltsL))
		voltsM = irSensors.readADCSingleEnded(1,gain,sps)/1000
		distanceM.append(irDistFront(voltsM))
		voltsR = irSensors.readADCSingleEnded(2,gain,sps)/1000
		distanceR.append( irDistRight(voltsR))
		sleep(.5)

	final_distanceL = sum(distanceL)/len(distanceL)
	final_distanceM = sum(distanceM)/len(distanceM)
	final_distanceR = sum(distanceR)/len(distanceR)    
	print 'left: ' + str(final_distanceL)
	
	print 'front: ' + str(final_distanceM)
	
	print 'right: ' + str(final_distanceR)

	path_lst=[False]*3

	path_lst[0] = final_distanceL > 20
	path_lst[1] = final_distanceM > 20
	path_lst[2] = final_distanceR > 20
	
	return path_lst 

''' 
*** NOTE ***
Left: Dark Green 2Y0A21
Front: 2D120X
Right: Light Green 2Y0A21
'''
'''
def irDistLeft(volts):
	# Function to calculate distance from right sensor
	return 26.47 * volts**(-1.185)

def irDistFront(volts):
	return 26.46 * volts**(-1.2)

def irDistRight(volts):
	# Function to calculate distance from left sensor
	return 26.453 * volts**(-1.221)
'''

def irDistLeft(volts):
	return 11.721 * volts**(-0.972)

def irDistFront(volts):
	if volts == 0:
		return 
	else:
		return 11.721 * volts**(-0.972)

def irDistRight(volts):
	if volts == 0:
		return 1
	else:
		return 11.721 * volts**(-0.972)


def checkItem():
	# Check if there's an item
	itemFound = pixyDetectItem()

	if itemFound == 'gift':
		giftFound = True
		pickUpGift()

		if treeFound: 
			# Exit and navigate to the tree
		    pass

	elif itemFound == 'tree':
		treeFound = True

		if giftFound:
			dropGift()
			giftDropped = True
			
		turnList = {1: 'G'}
		turnIndex = 2

def pixyDetectItem():

	item = ''

	if digitalRead(TREE_PIN):
		item = 'tree'
	elif digitalRead(GIFT_PIN):
		item = 'gift'

	return item

def pickUpGift():
	print 'picking up'
	servoControl.set_pwm(SERVO_PINCH, 0, OPEN_SERVO)
	sleep(1)
	servoControl.set_pwm(SERVO_LIFT, 0, LOWER_SERVO)
	sleep(1)
	servoControl.set_pwm(SERVO_PINCH,0, CLOSE_SERVO)
	sleep(1)
	servoControl.set_pwm(SERVO_LIFT, 0, RAISE_SERVO)
	sleep(1)

def dropGift():
	print 'dropping'
	servoControl.set_pwm(SERVO_LIFT, 0, LOWER_SERVO)
	sleep(1)
	servoControl.set_pwm(SERVO_PINCH, 0, OPEN_SERVO)
	sleep(1)
	servoControl.set_pwm(SERVO_LIFT, 0, RAISE_SERVO)
	sleep(1)
	servoControl.set_pwm(SERVO_PINCH, 0, CLOSE_SERVO)
	sleep(1)

# Initialize first node
map_dic={1:[[0,0,0],[0,0,0],0,'N']}

# Initialize tree_lst: current = 1, previous = 0, highest index = 1, direction = forward
tree_lst=[1,0,1,'f']

# Initialize path_lst: assume facing forward at start
path_lst=[False,True,False] 

# Initialize that tree and gift have not been found
giftFound = False
treeFound = False
giftDropped = False

# Create second node based on initialized tree_lst and path_lst
mapping.node_proc(map_dic, tree_lst, path_lst)

# Print current structure
mapping.print_node(map_dic)

while True:
	sleep(.5)
	moveRobotForward()

	path_lst = update_intersection(irSensors)

	# Check if left turn is available
	if path_lst[0]:
		turnRobotLeft()
		
		# If at an intersection, add node to structure
		if path_lst[1] or path_lst[2]:
			mapping.node_proc(map_dic, tree_lst, path_lst)

		# Mark opposite turn if tree is found
		if treeFound:
			if tree_lst[2]:
				turnList[turnIndex] = 'R'
				turnIndex += 1
			else:
				turnIndex -= 1
				del turnList[turnIndex]

	# Check if straight is available
	elif path_lst[1]:
		# Keep robot straight

		if path_lst[2]:
			mapping.node_proc(map_dic, tree_lst, path_lst)

		# Mark middle if tree is found
		if treeFound:
			if tree_lst[2] == 'f':
				turnList[turnIndex] = 'M'
				turnIndex += 1
			else:
				turnIndex -= 1
				del turnList[turnIndex]

	# Check if right is available
	elif path_lst[2]:
		turnRobotRight()

		# Mark opposite turn if tree is found
		if treeFound:
			if tree_lst[2]:
				turnList[turnIndex] = 'L'
				turnIndex += 1
			else:
				turnIndex -= 1
				del turnList[turnIndex]

	# Deadend has been reached
	else:

		# Swap current node and previous node
		temp = tree_lst[1]
		tree_lst[1] = tree_lst[0]
		tree_lst[0] = temp

		# Change direction
		tree_lst[2] = 'b'



