import RPi.GPIO as GPIO
import time

class HotWire:
    def __init__(self,PIN):
        GPIO.setmode(GPIO.BOARD)
        self.pin=PIN
        GPIO.setup(PIN, GPIO.OUT)

    def activate(self):
        GPIO.output(self.pin,True)
        time.sleep(1.5)
        GPIO.output(self.pin,False)
