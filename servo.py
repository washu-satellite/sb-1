import RPi.GPIO as GPIO
from time import sleep
from constants import SERVO_MAX_DUTY, SERVO_MIN_DUTY
class Servo:
    def __init__(self, PIN, initial):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIN, GPIO.OUT)
        
        self.pin = GPIO.PWM(PIN, 50)
        self.pin.start(initial)
        self.pwm = initial
        sleep(0.01)

    # Rotates camera viewport by 'angle' degrees
    def swivel(self, angle):
        pwm = self.compute_delta(angle)
        if pwm < SERVO_MIN_DUTY:
            pwm = SERVO_MIN_DUTY
        elif pwm > SERVO_MAX_DUTY:
            pwm = SERVO_MAX_DUTY
        
        self.pin.ChangeDutyCycle(pwm)


    def compute_delta(self, theta):
        return self.pwm + theta/180*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)
        
