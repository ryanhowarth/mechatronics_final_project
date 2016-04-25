import pigpio
import rotary_encoder

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