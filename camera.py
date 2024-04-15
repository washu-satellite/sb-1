"""

Abstraction layer for camera operations including rotation and image capture

authors: nathanielhayman@gmail.com

"""

import RPi.GPIO as GPIO
import time
import argparse
import cv2
import numpy as np
from picamera2 import Picamera2

from constants import PIN_SERVO_MAJOR, PIN_SERVO_MINOR, PWM_PIN_SERVO_MAJOR, 
                      PWM_PIN_SERVO_MINOR


class Camera:
    
    def __init__(self):
        self.cam = Picamera2()
        self.cam.start()
        
        print(cam)
        
        GPIO.setup(PIN_SERVO_MAJOR, GPIO.OUT)
        GPIO.setup(PIN_SERVO_MINOR, GPIO.OUT)
        
        self.servo_major = GPIO.PWM(PIN_SERVO_MAJOR, 50)
        self.servo_minor = GPIO.PWM(PIN_SERVO_MINOR, 50)
        
        self.servo_major.start(PWM_PIN_SERVO_MAJOR)
        self.servo_minor.start(PWM_PIN_SERVO_MINOR)
        
        self.cam_servos = [servo_major, servo_minor]
    
    
    # Rotates camera viewport by `angle` degrees
    def swivel(angle):
        # TODO: create a protocol for rotating the indivudal servos
        # in the camera dual-servo system
        granular_swivel(0, angle)
        granular_swivel(1, angle)
        
    
    def granular_swivel(component, angle):
        
        if component < 0 or component > len(cam_servos):
            print(f"ERROR: unknown camera rotation component {component}! \
                    valid components lie in the range 0->{len(cam_servos)}")
        
        pwm = compute_delta(angle)
        
        self.cam_servos[component].ChangeDutyCycle(pwm)


    def compute_delta(theta):
        # TODO: determine appropriate theta -> PWM formula based
        # on servo responsiveness
        return -1
    
    
    # Captures an image with the camera and uploads it to
    # `./captures/history/capture_<t>_<i>.png` as well as
    # `./captures/recent_capture_<t>.png`.
    #
    # Implicitly archives previous capture
    def capture_image(is_termination, itr):
        array = cam.capture_array("main")
        arraybgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        
        cv2.imwrite(f"captures/history/capture_{is_termination}_{itr % 10}.png", arraybgr)
        cv2.imwrite("captures/f"capture_{is_termination}.png""+fname, arraybgr)


    def __del__(self):
        cam.stop()
        servo_major.stop()
        servo_minor.stop()
    
