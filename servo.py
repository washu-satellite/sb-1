import RPi.GPIO as GPIO

class Servo:
    def __init__(self, PIN, initial):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIN, GPIO.OUT)
        
        self.pin = GPIO.PWM(PIN, 50)
        self.pin.start(initial)
        self.pwm = initial

    # Rotates camera viewport by 'angle' degrees
    def swivel(self, angle):
        pwm = self.compute_delta(angle)
        if pwm < 10:
            pwm = 10
        elif pwm > 90:
            pwm = 90
        
        self.pin.ChangeDutyCycle(pwm)


    def compute_delta(self, theta):
        return self.pwm + theta/180*100
        