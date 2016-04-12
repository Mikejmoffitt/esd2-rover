import pigpio
import time

pi = pigpio.pi()

DUTY_MIN = 25
PWM_FREQ = 1000

DIR_FWD = 0
DIR_BACK = 1

SIDE_R = 0
SIDE_L = 1

MOTOR_R1_DIR = 19
MOTOR_R2_DIR = 27
MOTOR_L1_DIR = 5
MOTOR_L2_DIR = 6

MOTOR_R1_PWM = 26
MOTOR_R2_PWM = 22
MOTOR_L1_PWM = 17
MOTOR_L2_PWM = 4

DEADSTOP_COEF = 0.07


class motor_controller():
	# Dead stop variables
	motor_r_speed = 0
	motor_l_speed = 0
	motor_r_dir = 0
	motor_l_dir = 0
	
	def __init__(self):
		pi.set_PWM_frequency(MOTOR_R1_PWM, PWM_FREQ)
		pi.set_PWM_frequency(MOTOR_L1_PWM, PWM_FREQ)
		pi.set_PWM_frequency(MOTOR_R2_PWM, PWM_FREQ)
		pi.set_PWM_frequency(MOTOR_L2_PWM, PWM_FREQ)
		
		pi.set_PWM_range(MOTOR_R1_PWM, 100)
		pi.set_PWM_range(MOTOR_L1_PWM, 100)
		pi.set_PWM_range(MOTOR_R2_PWM, 100)
		pi.set_PWM_range(MOTOR_L2_PWM, 100)
		
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
		calc_delay = DEADSTOP_COEF * (self.motor_r_speed + self.motor_l_speed) / 200.0
			
		print "Using " + str(calc_delay) + "for deadstop time"
			
		# do the action
		self.set_dir(SIDE_R, self.motor_r_dir)
		self.set_dir(SIDE_L, self.motor_l_dir)
		time.sleep(calc_delay)
	
	def shutdown(self):
		self.set_speed(SIDE_R, 0)
		self.set_speed(SIDE_L, 0)

	def set_dir(self, side, dir):
		if (side == SIDE_R):
			self.motor_r_dir = dir;
			pi.write(MOTOR_R1_DIR, dir)
			pi.write(MOTOR_R2_DIR, 0 if dir else 1)
		elif (side == SIDE_L):
			self.motor_l_dir = dir;
			pi.write(MOTOR_L1_DIR, dir)
			pi.write(MOTOR_L2_DIR, 0 if dir else 1)
		
	def set_speed(self, side, speed):
		if (speed != 0 and speed < DUTY_MIN):
			speed = DUTY_MIN;
		if (side == SIDE_R):
			self.motor_r_speed = speed;
			pi.set_PWM_dutycycle(MOTOR_R1_PWM, speed)
			pi.set_PWM_dutycycle(MOTOR_R2_PWM, speed)
		elif (side == SIDE_L):
			self.motor_l_speed = speed;
			pi.set_PWM_dutycycle(MOTOR_L1_PWM, speed)
			pi.set_PWM_dutycycle(MOTOR_L2_PWM, speed)

my_motor = motor_controller();

my_motor.set_dir(SIDE_R, DIR_FWD)
my_motor.set_dir(SIDE_L, DIR_FWD)
my_motor.set_speed(SIDE_R, 100);
my_motor.set_speed(SIDE_L, 100);

time.sleep(1)
my_motor.dead_stop()
my_motor.shutdown()