"""

Core operation management for Small Balloon 1 (sb1)

"""

import time
import argparse
import RPi.GPIO as GPIO
import camera

DELAY_CAM_CAPTURE = 0.1


def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    
    print("init camera")
    
    parse_arguments()
    
    camera.init()
    
    # GPIO.setup(PWM_pin, GPIO.OUT)
    

def parse_arguments():
    global args
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--min", action="store", type=int, default=2)
    parser.add_argument("--max", action="store", type=int, default=12)
    parser.add_argument("--tim", action="store", type=int, default=30)
    parser.add_argument("--delay", action="store", type=int, default=1)

    args = parser.parse_args()
    
    return

# Captures a snapshot of data from NEO-6M GPS receiver
# with the following format:
#
# { type: string,  }
def get_gps_data():
    return

def send_status():
    return

def init_termination():
    return

def tick():
    return

def close():
    camera.destroy()

args = None

init()

start_time = time.time()
cur_time = start_time

last_cam_capture = start_time
itr = 0

while cur_time < start_time + args.tim:
    cur_time = time.time()
    
    if last_cam_capture + DELAY_CAM_CAPTURE < cur_time:
        
        if args.debug:
            print("IMAGE TAKEN")
        
        camera.capture_image(False, itr)
        
        last_cam_capture = cur_time
        
        itr += 1
        
close()