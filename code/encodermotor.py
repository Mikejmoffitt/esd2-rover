import pigpio
import time
from constants import *

# Motor control class
# ===================
# Abstracts motors into controlling the rover's sides to go forwards and back
# This one uses encoder ticks.

BALANCE_HI = 2
BALANCE_LOW = 20

pi= pigpio.pi()

motor_r_cnt = 0
motor_l_cnt = 0
motor_r_dir = 0
motor_l_dir = 0
motor_balance = 0

MOTOR_FULLSPEED = 24
MOTOR_HALFSPEED = 14

def check_r_distance():
	global motor_balance
	global motor_r_cnt
	# Halt if this motor's distance is satisfied
	if (motor_r_cnt > 0):
		
		# Slow down this motor if the balance is far off
		if (motor_balance > BALANCE_HI):
			pi.set_PWM_dutycycle(MOTOR_R1_PWM, MOTOR_HALFSPEED)
			pi.set_PWM_dutycycle(MOTOR_R2_PWM, MOTOR_HALFSPEED)
			pi.set_PWM_dutycycle(MOTOR_L1_PWM, MOTOR_FULLSPEED)
			pi.set_PWM_dutycycle(MOTOR_L2_PWM, MOTOR_FULLSPEED)
		# Return to normalcy
		else: #if (motor_balance <= BALANCE_LOW):
			pi.set_PWM_dutycycle(MOTOR_R1_PWM, MOTOR_FULLSPEED)
			pi.set_PWM_dutycycle(MOTOR_R2_PWM, MOTOR_FULLSPEED)
			pi.set_PWM_dutycycle(MOTOR_L1_PWM, MOTOR_HALFSPEED)
			pi.set_PWM_dutycycle(MOTOR_L2_PWM, MOTOR_HALFSPEED)
		if (motor_r_cnt == 0):
			pi.set_PWM_dutycycle(MOTOR_R1_PWM, 0)
			pi.set_PWM_dutycycle(MOTOR_R2_PWM, 0)
	else:
		print "STOPPING R."
		pi.set_PWM_dutycycle(MOTOR_R1_PWM, 0)
		pi.set_PWM_dutycycle(MOTOR_R2_PWM, 0)

def check_l_distance():
	global motor_balance
	global motor_l_cnt
	# Halt if this motor's distance is satisfied
	if (motor_l_cnt > 0):

		# Slow down this motor if the balance is far off
		if (motor_balance < BALANCE_HI * -1):
			pi.set_PWM_dutycycle(MOTOR_L1_PWM, MOTOR_HALFSPEED)
			pi.set_PWM_dutycycle(MOTOR_L2_PWM, MOTOR_HALFSPEED)
			pi.set_PWM_dutycycle(MOTOR_R1_PWM, MOTOR_FULLSPEED)
			pi.set_PWM_dutycycle(MOTOR_R2_PWM, MOTOR_FULLSPEED)
		# Return to normalcy
		else: #if (motor_balance >= BALANCE_LOW * -1):
			pi.set_PWM_dutycycle(MOTOR_L1_PWM, MOTOR_FULLSPEED)
			pi.set_PWM_dutycycle(MOTOR_L2_PWM, MOTOR_FULLSPEED)
			pi.set_PWM_dutycycle(MOTOR_R1_PWM, MOTOR_HALFSPEED)
			pi.set_PWM_dutycycle(MOTOR_R2_PWM, MOTOR_HALFSPEED)
		if (motor_l_cnt == 0):
			pi.set_PWM_dutycycle(MOTOR_L1_PWM, 0)
			pi.set_PWM_dutycycle(MOTOR_L2_PWM, 0)
	else:
		print "STOPPING L."
		pi.set_PWM_dutycycle(MOTOR_L1_PWM, 0)
		pi.set_PWM_dutycycle(MOTOR_L2_PWM, 0)


def right_callback(a,b,c):
	global motor_balance
	global motor_r_cnt
	if (motor_r_cnt > 0):
		motor_r_cnt = motor_r_cnt - 1
		motor_balance = motor_balance + 1
		

def left_callback(a,b,c):
	global motor_balance
	global motor_l_cnt
	if (motor_l_cnt > 0):
		motor_l_cnt = motor_l_cnt - 1
		motor_balance = motor_balance - 1
		

cbr = pi.callback(ENCODER_R, pigpio.RISING_EDGE, right_callback)
cbl = pi.callback(ENCODER_L, pigpio.RISING_EDGE, left_callback)

class motor_controller():
	
	def __init__(self):
		print "Motor initialized"
		self.pi = pi
		self.pi.set_PWM_frequency(MOTOR_R1_PWM, PWM_FREQ)
		self.pi.set_PWM_frequency(MOTOR_L1_PWM, PWM_FREQ)
		self.pi.set_PWM_frequency(MOTOR_R2_PWM, PWM_FREQ)
		self.pi.set_PWM_frequency(MOTOR_L2_PWM, PWM_FREQ)
		
		self.pi.set_PWM_range(MOTOR_R1_PWM, 100)
		self.pi.set_PWM_range(MOTOR_L1_PWM, 100)

		self.pi.set_PWM_range(MOTOR_R2_PWM, 100)
		self.pi.set_PWM_range(MOTOR_L2_PWM, 100)
		

		self.stop()

	def wait_complete(self):
		while (motor_r_cnt > 0 or motor_l_cnt > 0):
			pass

	def shutdown(self):
		self.stop()

	def dead_stop(self):
		global motor_r_dir
		global motor_l_dir
		global motor_balance
		# Reverse directions
		if (motor_r_dir == DIR_FWD):
			motor_r_dir = DIR_BACK
		else:
			motor_r_dir = DIR_FWD
			
		if (motor_l_dir == DIR_FWD):
			motor_l_dir = DIR_BACK
		else:
			motor_l_dir = DIR_FWD
			
		# calculate delay time based on top speed
		calc_delay = 0.07
			
		# briefly engage the reverse direction
		self.pi.write(MOTOR_R1_DIR, motor_r_dir)
		self.pi.write(MOTOR_R2_DIR, 0 if motor_r_dir else 1)
		self.pi.write(MOTOR_L1_DIR, motor_l_dir)
		self.pi.write(MOTOR_L2_DIR, 0 if motor_l_dir else 1)

		# run in reverse for the calculated delay time
		time.sleep(calc_delay)

		# stop motors
		self.stop()

	# Set a side's speed in percentage (really the PWM duty)
	def fwd(self, count):
		print "Motor forward " + str(count) + " ticks."
		global motor_balance
		global motor_r_cnt
		global motor_l_cnt
		incomplete = 1
		motor_balance = 0
		motor_r_cnt = int(count)
		motor_l_cnt = int(count)

		motor_r_dir = 0
		motor_l_dir = 0

		self.pi.write(MOTOR_R1_DIR, 0)
		self.pi.write(MOTOR_R2_DIR, 1)
		self.pi.write(MOTOR_L1_DIR, 0)
		self.pi.write(MOTOR_L2_DIR, 1)

		self.pi.set_PWM_dutycycle(MOTOR_R1_PWM, MOTOR_FULLSPEED)
		self.pi.set_PWM_dutycycle(MOTOR_R2_PWM, MOTOR_FULLSPEED)
		self.pi.set_PWM_dutycycle(MOTOR_L1_PWM, MOTOR_FULLSPEED)
		self.pi.set_PWM_dutycycle(MOTOR_L2_PWM, MOTOR_FULLSPEED)

		while (motor_r_cnt != 0 or motor_l_cnt != 0):
			check_r_distance()
			check_l_distance()
			print "Bal: " + str(motor_balance) + ", R: " + str(motor_r_cnt) + ", L: " + str(motor_l_cnt)
			time.sleep(0.001)

	# Set a side's speed in percentage (really the PWM duty)
	def ror(self, count):
		motor_balance = 0
		motor_r_cnt = count
		motor_l_cnt = count
		
		motor_r_dir = 1
		motor_l_dir = 0

		self.pi.write(MOTOR_R1_DIR, 0)
		self.pi.write(MOTOR_R2_DIR, 1)
		self.pi.write(MOTOR_L1_DIR, 1)
		self.pi.write(MOTOR_L2_DIR, 0)

		self.pi.set_PWM_dutycycle(MOTOR_R1_PWM, 100)
		self.pi.set_PWM_dutycycle(MOTOR_R2_PWM, 100)
		self.pi.set_PWM_dutycycle(MOTOR_L1_PWM, 100)
		self.pi.set_PWM_dutycycle(MOTOR_L2_PWM, 100)
		
	# Set a side's speed in percentage (really the PWM duty)
	def back(self, count):
		motor_balance = 0
		motor_r_cnt = count
		motor_l_cnt = count
		
		motor_r_dir = 1
		motor_l_dir = 1

		self.pi.write(MOTOR_R1_DIR, 1)
		self.pi.write(MOTOR_R2_DIR, 0)
		self.pi.write(MOTOR_L1_DIR, 1)
		self.pi.write(MOTOR_L2_DIR, 0)

		self.pi.set_PWM_dutycycle(MOTOR_R1_PWM, 100)
		self.pi.set_PWM_dutycycle(MOTOR_R2_PWM, 100)
		self.pi.set_PWM_dutycycle(MOTOR_L1_PWM, 100)
		self.pi.set_PWM_dutycycle(MOTOR_L2_PWM, 100)


	def stop(self):
		motor_r_cnt = 0
		motor_l_cnt = 0
		motor_balance = 0

		self.pi.set_PWM_dutycycle(MOTOR_R1_PWM, 0)
		self.pi.set_PWM_dutycycle(MOTOR_R2_PWM, 0)
		self.pi.set_PWM_dutycycle(MOTOR_L1_PWM, 0)
		self.pi.set_PWM_dutycycle(MOTOR_L2_PWM, 0)
