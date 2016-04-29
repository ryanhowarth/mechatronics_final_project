	def goStraight(self):
		self.motorL.forward()
		self.motorR.forward()
		
		self.motorL.setSpeed(PWM_DEFAULT)
		self.motorR.setSpeed(PWM_DEFAULT)

	#@profile
	def move_robot(self, decision):

		ir_data = self.getIrSensorData()
		# Waiting to exit previous intersection
		wallToFollow = decision
		while ir_data[decision] > 25:
			# Follow opposite wall if it exists
			if ir_data[(decision + 2) % 4] < 20:
				self.followWall( (decision + 2) % 4)
			# Otherwise go straight
			else:
				self.goStraight()
			ir_data = self.getIrSensorData()
		self.stop()

		# While walls exist on both sides, 
		# follow the wall we came from
		while (ir_data[0] < 25) and (ir_data[2] < 25):
			self.followWall(wallToFollow)
			ir_data = self.getIrSensorData()
		self.stop()

	def step_forward(self, wallToFollow)		
	
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
		ir_data = self.getIrSensorData()
                print (ir_data)

		# Case that should rarely (never) happen
               	if middle_ir < 8:
                       	return ir_data

              	R_pwm_speed = PWM_DEFAULT
               	L_pwm_speed = PWM_DEFAULT

		# Proportional control of motors
		if ir_data[wallToFollow] < 20:
			magnitude = 16 - ir_data[wallToFollow]
			if wallToFollow == 0:
				L_pwm_speed += magnitude * GAIN
                        	R_pwm_speed -= magnitude * GAIN
			elif wallToFollow == 2:
				R_pwm_speed += magnitude * GAIN
				L_pwm_speed -= magnitude * GAIN
            		
		# Constrain PWM to constants
               	if R_pwm_speed > PWM_MAX:
                    	R_pwm_speed = PWM_MAX
       		elif R_pwm_speed < PWM_MIN:
                      	R_pwm_speed = PWM_MIN
            	if L_pwm_speed > PWM_MAX:
                       	L_pwm_speed = PWM_MAX
               	elif L_pwm_speed < PWM_MIN:
                     	L_pwm_speed = PWM_MIN

		# Set motor speeds
             	self.leftMotor.setSpeed(L_pwm_speed)
            	self.rightMotor.setSpeed(R_pwm_speed)
              	
		return ir_data
	
