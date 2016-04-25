
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

