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

from constants import PIN_SERVO_MAJOR, PIN_SERVO_MINOR, PWM_PIN_SERVO_MAJOR, PWM_PIN_SERVO_MINOR


class Camera:
    
    def __init__(self):
        self.cam = Picamera2()
        self.cam.start()
        
        print(self.cam)

    # Captures an image with the camera and uploads it to
    # `./captures/history/capture_<t>_<i>.png` as well as
    # `./captures/recent_capture_<t>.png`.
    #
    # Implicitly archives previous capture
    def capture_image(self, is_termination, itr):
        array = self.cam.capture_array("main")
        arraybgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        
        cv2.imwrite(f"captures/history/capture_{is_termination}_{itr % 10}.png", arraybgr)
        cv2.imwrite(f"captures/capture_{is_termination}.png", arraybgr)


    def __del__(self):
        self.cam.stop()
    
