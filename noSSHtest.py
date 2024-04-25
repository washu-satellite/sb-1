from constants import PIN_SERVO_MAJOR,PIN_SERVO_MINOR, SERVO_MAX_DUTY, SERVO_MIN_DUTY, DELAY_CAM_CAPTURE, PARACHUTE_PIN,FAILSAFE_PIN
from servo import Servo
import time

servoPan = Servo(PIN_SERVO_MAJOR, (SERVO_MAX_DUTY + SERVO_MIN_DUTY)/2)
count=0
while(True):
    count +=1
    time.sleep(.5)
    servoPan.swivel(90)
    time.sleep(.5)
    servoPan.swivel(-90)
    print(f"count: {count}")