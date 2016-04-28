from encodermotor import motor_controller
from constants import *
import time
import sys
import signal

motors = motor_controller()

def signal_handler(signal, frame):
	print("SIGINT received, killing motors.")
	motors.stop()
	sys.exit()

def main():
	signal.signal(signal.SIGINT, signal_handler)
	motors.fwd(20)
	motors.wait_complete()
	time.sleep(1.0)

if __name__ == "__main__":
	main()
