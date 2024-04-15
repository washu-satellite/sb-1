"""

Controller for the NEO-6M GPS receiver

authors: nathanielhayman@gmail.com

"""

import serial
import time
import string
import pynmea2


class GPSController:
    
    __init__(self):
        port="/dev/ttyAMA0"
        
        self.serial = serial.Serial(port, baudrate=9600, timeout=0.5)
        self.data_out = pynmea2.NMEAStreamReader()
    
    # Captures a snapshot of various data from serial stream
    def data_snapshot():
        data = self.serial.readline()
        
        if data[0:6] == "$GPRMC":
            msg = pynmea2.parse(data)
            
            return {"lat": msg.latitude, "lng": msg.longitude}
        