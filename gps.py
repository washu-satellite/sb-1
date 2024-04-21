"""

Controller for the NEO-6M GPS receiver

authors: nathanielhayman@gmail.com

"""

import serial
import time
import string
import pynmea2


class GPSController:  
    LATITUDE_INDEX=2
    LONGITUDE_INDEX=4
    ALTITUDE_INDEX=9

    def __init__(self):
        port="/dev/ttyAMA0"
        self.serial = serial.Serial(port, baudrate=9600, timeout=0.5)
        self.data_out = pynmea2.NMEAStreamReader()
    
    # Captures a snapshot of various data from serial stream
    def data_snapshot(self):
        data = self.serial.readline()
        if data[0:6] == b'$GPGGA':
            #changes that may or not may work, keeping the original code commented out below
            split_data = data.decode('utf-8').split(",")
            lat=float(split_data[2])
            long=float(split_data[4])
            alt=float(split_data[9])
            print("long: ")
            print(long)
            return lat,long,alt
            #msg = pynmea2.parse(data)
            
            # return {"lat": msg.latitude, "lng": msg.longitude}
        return None, None, None


