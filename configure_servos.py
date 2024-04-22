from constants import PIN_SERVO_MAJOR, PIN_SERVO_MINOR
import argparse
import RPi.GPIO as GPIO
from time import sleep
parser = argparse.ArgumentParser()

parser.add_argument("--smajor", action="store", type=int, default=50)
parser.add_argument("--sminor", action="store", type=int, default=50)

args = parser.parse_args()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_SERVO_MAJOR, GPIO.OUT)
GPIO.setup(PIN_SERVO_MINOR, GPIO.OUT)

servo_major = GPIO.PWM(PIN_SERVO_MAJOR, 50)
servo_minor = GPIO.PWM(PIN_SERVO_MINOR, 50)

servo_major.start(args.smajor)
servo_minor.start(args.sminor)
sleep(5)
GPIO.cleanup()
