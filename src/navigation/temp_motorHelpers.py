
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


