"""

SB1 dynamic controller

authors: nathanielhayman@gmail.com

"""


import time

from constants import DELAY_CAM_CAPTURE


class Controller:
    
    __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        self.args = parse_arguments()
        
        self.camera = Camera()
    
    
    def parse_arguments():
        parser = argparse.ArgumentParser()
        
        parser.add_argument("--debug", action="store_true")
        parser.add_argument("--min", action="store", type=int, default=2)
        parser.add_argument("--max", action="store", type=int, default=12)
        parser.add_argument("--tim", action="store", type=int, default=30)
        parser.add_argument("--delay", action="store", type=int, default=1)

        return parser.parse_args()
    
    
    def iterate():
        start_time = time.time()
        cur_time = start_time

        last_cam_capture = start_time
        itr = 0

        while cur_time < start_time + args.tim:
            cur_time = time.time()
            
            if last_cam_capture + DELAY_CAM_CAPTURE < cur_time:
                
                if args.debug:
                    print("IMAGE TAKEN")
                
                self.camera.capture_image(False, itr)
                
                last_cam_capture = cur_time
                
                itr += 1
                
    
    def __del__(self):
        camera.destroy()
