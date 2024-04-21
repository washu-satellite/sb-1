"""

SB1 dynamic controller

authors: nathanielhayman@gmail.com

"""


import time
import RPi.GPIO as GPIO
import argparse
from constants import DELAY_CAM_CAPTURE
from camera import Camera
from servo import Servo


class Controller:
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        self.args = self.parse_arguments()
        
        self.camera = Camera()
    
    
    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        
        parser.add_argument("--debug", action="store_true")
        parser.add_argument("--min", action="store", type=int, default=2)
        parser.add_argument("--max", action="store", type=int, default=12)
        parser.add_argument("--tim", action="store", type=int, default=30)
        parser.add_argument("--delay", action="store", type=int, default=1)

        return parser.parse_args()
    
    
    def iterate(self):
        start_time = time.time()
        cur_time = start_time

        last_cam_capture = start_time
        itr = 0

        while cur_time < start_time + self.args.tim:
            cur_time = time.time()
            
            if last_cam_capture + DELAY_CAM_CAPTURE < cur_time:
                
                if self.args.debug:
                    print("IMAGE TAKEN")
                
                self.camera.capture_image(False, itr)
                
                last_cam_capture = cur_time
                
                itr += 1
                
    
    def __del__(self):
        del self.camera

