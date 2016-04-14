import pigpio
import time
from constants import *

# Motor control class
# ===================
# Abstracts motors into controlling the rover's sides to go forwards and back
# at various speeds, reducing coupling to the hardware itself.
# 
# Instantiate a class like so:
#     motors = motor_controller()
#
# Then, commands may be issued:
#     motors.set_dir(SIDE_LEFT, DIR_FWD)
#     motors.set_speed(SIDE_LEFT, 70)
#     motors.dead_stop();
#     motors.shutdown();
#

class motor_controller():
	
	def __init__(self):
		self.pi= pigpio.pi()
		self.pi.set_PWM_frequency(MOTOR_R1_PWM, PWM_FREQ)
		self.pi.set_PWM_frequency(MOTOR_L1_PWM, PWM_FREQ)
		self.pi.set_PWM_frequency(MOTOR_R2_PWM, PWM_FREQ)
		self.pi.set_PWM_frequency(MOTOR_L2_PWM, PWM_FREQ)
		
		self.pi.set_PWM_range(MOTOR_R1_PWM, 100)
		self.pi.set_PWM_range(MOTOR_L1_PWM, 100)
		self.pi.set_PWM_range(MOTOR_R2_PWM, 100)
		self.pi.set_PWM_range(MOTOR_L2_PWM, 100)
		
		self.motor_r_dir = DIR_FWD
		self.motor_l_dir = DIR_FWD
		self.motor_r_speed = 0
		self.motor_l_speed = 0

	def dead_stop(self):
		# Reverse directions
		if (self.motor_r_dir == DIR_FWD):
			self.motor_r_dir = DIR_BACK
		else:
			self.motor_r_dir = DIR_FWD
			
		if (self.motor_l_dir == DIR_FWD):
			self.motor_l_dir = DIR_BACK
		else:
			self.motor_l_dir = DIR_FWD
			
		# calculate delay time based on top speed
		calc_delay = 0.07 * (float(self.motor_r_speed) + float(self.motor_l_speed)) / 200.0
			
		# briefly engage the reverse direction
		self.set_dir(SIDE_R, self.motor_r_dir)
		self.set_dir(SIDE_L, self.motor_l_dir)

		# run in reverse for the calculated delay time
		time.sleep(calc_delay)

		# stop motors
		self.set_speed(SIDE_R, 0);
		self.set_speed(SIDE_L, 0);

		# put the directions back
		if (self.motor_r_dir == DIR_FWD):
			self.motor_r_dir = DIR_BACK
		else:
			self.motor_r_dir = DIR_FWD
			
		if (self.motor_l_dir == DIR_FWD):
			self.motor_l_dir = DIR_BACK
		else:
			self.motor_l_dir = DIR_FWD

	# Make the motors stop turning
	def shutdown(self):
		self.set_speed(SIDE_R, 0)
		self.set_speed(SIDE_L, 0)

	# Set a side to go forwards or backwards
	def set_dir(self, side, dir):
		if (side == SIDE_R):
			self.motor_r_dir = dir;
			self.pi.write(MOTOR_R1_DIR, dir)
			self.pi.write(MOTOR_R2_DIR, 0 if dir else 1)
		elif (side == SIDE_L):
			self.motor_l_dir = dir;
			self.pi.write(MOTOR_L1_DIR, dir)
			self.pi.write(MOTOR_L2_DIR, 0 if dir else 1)
		
	# Set a side's speed in percentage (really the PWM duty)
	def set_speed(self, side, speed):
		if (speed != 0 and speed < DUTY_MIN):
			speed = DUTY_MIN;
		if (side == SIDE_R):
			self.motor_r_speed = speed;
			self.pi.set_PWM_dutycycle(MOTOR_R1_PWM, speed)
			self.pi.set_PWM_dutycycle(MOTOR_R2_PWM, speed)
		elif (side == SIDE_L):
			self.motor_l_speed = speed;
			self.pi.set_PWM_dutycycle(MOTOR_L1_PWM, speed)
			self.pi.set_PWM_dutycycle(MOTOR_L2_PWM, speed)
