import RPi.GPIO as GPIO
import time
import argparse
import cv2
import numpy
from picamera2 import Picamera2


PIN_SERVO_MAJOR = 33
PIN_SERVO_MINOR = 32

PWM_PIN_SERVO_MAJOR = 5
PWM_PIN_SERVO_MINOR = 5

servo_major = None
servo_minor = None

cam_servos = []

cam = None

def init():
    global cam, cam_servos, servo_major, servo_minor
    
    cam = Picamera2()
    cam.start()
    
    print(cam)
    
    GPIO.setup(PIN_SERVO_MAJOR, GPIO.OUT)
    GPIO.setup(PIN_SERVO_MINOR, GPIO.OUT)
    
    servo_major = GPIO.PWM(PIN_SERVO_MAJOR, 50)
    servo_minor = GPIO.PWM(PIN_SERVO_MINOR, 50)
    
    servo_major.start(PWM_PIN_SERVO_MAJOR)
    servo_minor.start(PWM_PIN_SERVO_MINOR)
    
    cam_servos = [servo_major, servo_minor]


# Rotates camera servos by `angle` degrees
def swivel(component, angle):
    pwm = compute_delta(angle)
    
    if component < 0 or component > len(cam_servos):
        print(f"ERROR: unknown camera rotation component {component}! \
                valid components lie in the range 0->{len(cam_servos)}")
    
    cam_servos[component].ChangeDutyCycle(pwm)

# Captures an image with the camera and uploads it to
# `./captures/capture<x.x>.png` as well as `./recent_capture.png`.
#
# Implicitly archives previous capture
def capture_image(is_termination, itr):
    array = cam.capture_array("main")
    arraybgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    
    fname = f"capture_{is_termination}.png"
    
    cv2.imwrite(fname, arraybgr)
    cv2.imwrite("captures/"+fname, arraybgr)
    

def compute_delta(theta):
    return

def destroy():
    global cam
    
    cam.stop()
    servo_major.stop()
    servo_minor.stop()
    