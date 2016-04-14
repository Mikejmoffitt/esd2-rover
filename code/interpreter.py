# Very simple rover "recipe" runtime
from motor import motor_controller
from constants import *
import time
import sys

def handle_line(motors, line):
	print "> " + line
	line = line.lower().rstrip(' \n').lstrip()
	line = line.split(' ')

	# Identify side(s) being commanded
	motor_r_en = False
	motor_l_en = False

	if (len(line[0]) < 1):
		print "DONE"
		return

	if "#" in line[0]:
		return

	if "r" in line[0]:
		motor_r_en = True
	
	if "l" in line[0]:
		motor_l_en = True
	
	if "deadstop" in line[0]:
		motors.dead_stop()
	elif "stop" in line[0]:
		motors.shutdown()
	elif "wait" in line[0]:
		if len(line[1]) > 0:
			time.sleep(float(line[1]))
	else:
		# Determine which command is run
		cmd = line[1];
		print "Running " + cmd
		if "fwd" in cmd or "forward" in cmd:
			if (motor_r_en == True):
				print "Right motor fwd"
				motors.set_dir(SIDE_R, DIR_FWD)
				motors.set_speed(SIDE_R, line[2])
			if (motor_l_en == True):
				print "Left motor fwd"
				motors.set_dir(SIDE_L, DIR_FWD)
				motors.set_speed(SIDE_L, line[2])
		elif "back" in cmd:
			if (motor_r_en == True):
				print "Right motor back"
				motors.set_dir(SIDE_R, DIR_BACK)
				motors.set_speed(SIDE_R, line[2])
			if (motor_l_en == True):
				print "Left motor back"
				motors.set_dir(SIDE_L, DIR_BACK)
				motors.set_speed(SIDE_L, line[2])
	print "-----------------\n"

def run_recipe(motors, recipename):
	motors.dead_stop()
	print "Opening " + recipename + "..."
	f = open(recipename, "r")
	lines = f.readlines()

	for line in lines:
		handle_line(motors, line)

def main():
	argc = len(sys.argv)
	if (argc < 2):
		print "Usage:"
		print sys.argv[0] + " [programfile]"
	else:
		motors = motor_controller()
		run_recipe(motors, sys.argv[1])

if __name__ == "__main__":
	main()
