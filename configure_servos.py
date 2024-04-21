from constants import PIN_SERVO_MAJOR, PIN_SERVO_MINOR, PWM_PIN_SERVO_MAJOR, PWM_PIN_SERVO_MINOR
import argparse
import RPi.GPIO as GPIO

parser = argparse.ArgumentParser()

parser.add_argument("--smajor", action="store", type=int, default=50)
parser.add_argument("--sminor", action="store", type=int, default=50)

args = parser.parse_args()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_SERVO_MAJOR, GPIO.OUT)
GPIO.setup(PIN_SERVO_MINOR, GPIO.OUT)

servo_major = GPIO.PWM(PIN_SERVO_MAJOR, args.smajor)
servo_minor = GPIO.PWM(PIN_SERVO_MINOR, args.sminor)

servo_major.start(PWM_PIN_SERVO_MAJOR)
servo_minor.start(PWM_PIN_SERVO_MINOR)
GPIO.cleanup()
