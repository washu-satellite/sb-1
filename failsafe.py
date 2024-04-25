import time
import sys
import select
from gps import GPSController
from servo import Servo
from hotWire import HotWire
from constants import PIN_SERVO_MAJOR,PIN_SERVO_MINOR, SERVO_MAX_DUTY, SERVO_MIN_DUTY, DELAY_CAM_CAPTURE, PARACHUTE_PIN,FAILSAFE_PIN
from camera import Camera

COUNTDOWN_SECONDS=15
listAverageSize=10
curListIndex=0
latList = [0]*listAverageSize
longList = [0]*listAverageSize
altList = [0]*listAverageSize
parachuteServo = Servo(PARACHUTE_PIN,(SERVO_MAX_DUTY + SERVO_MIN_DUTY)/2)
servoPan = Servo(PIN_SERVO_MAJOR, (SERVO_MAX_DUTY + SERVO_MIN_DUTY)/2)
servoTilt = Servo(PIN_SERVO_MINOR, (SERVO_MAX_DUTY + SERVO_MIN_DUTY)/2)
dummyPan = Servo(23,(SERVO_MAX_DUTY + SERVO_MIN_DUTY)/2)
# dummyTilt = Servo(21,(SERVO_MAX_DUTY + SERVO_MIN_DUTY)/2)
latVariance=.00067
longVariance=.00067
altVariance=150
GPS= GPSController()
cam = Camera()
failsafeWire = HotWire(FAILSAFE_PIN)

def initFailsafeCountdown():
    print()
    print("\\ \\        /     \\      _ \\   \\  |_ _|  \\  |  ___|")
    print(" \\ \\  \\   /     _ \\    |   |   \\ |  |    \\ | |  _  ")
    print("  \\ \\  \\ /     ___ \\   __ <  |\\  |  |  |\\  | |   |")
    print("   \\_/\\_/    _/    _\\ _| \\_\\_| \\_|___|_| \\_|\\____")
    print(f"averaged lat: {sum(latList)/listAverageSize} averaged long: {sum(longList)/listAverageSize} averaged alt: {sum(altList)/listAverageSize}")
    sys.stdout.write("Enter 'c' to halt the countdown: ")
    sys.stdout.flush()
def processData():
    global curListIndex
    lat,long,alt = getPositionData()
    if lat is not None:
        latList[curListIndex]=lat//100+(lat%100)/60
        longList[curListIndex]=long
        altList[curListIndex]=alt
        curListIndex+=1
        if(curListIndex>=listAverageSize):
            curListIndex=0
        return True
    return False
def getPositionData():
    return GPS.data_snapshot()
def activateFailsafe():
    print()
    print("  _|        _)  |                _|       ")
    print(" |     _` |  |  |   __|   _` |  |     _ \\ ")
    print(" _|   (   |  |  | \__ \\  (   |  _|    __/ ")
    print("_|   \\__._| _| _| ____/ \\__._| _|   \\___|")
    parachuteServo.swivel(-180)
    time.sleep(1)
    failsafeWire.activate()
def failsafeCountdown(initTime):
    while True:
        elapsed_time = time.time() - initTime
        remaining_time=COUNTDOWN_SECONDS - elapsed_time
        if remaining_time <= 0:
            activateFailsafe()
            break
        sys.stdout.write(f"\rEnter 'c' to abort: {remaining_time} seconds remaining: ")
        sys.stdout.flush()
        checkAbort()
def checkAbort():
    #outside!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    rlist, _, _ = select.select([sys.stdin], [], [], 1)
    if rlist:
        input_line = sys.stdin.readline().strip()
        if input_line.lower() == 'c':
            print("Failsafe Aborted")
            return True
def manualControls():
    sys.stdout.write(f"\rEnter 'k' to manually activate failsafe, 'pan/tilt <degrees>' to pan/tilt: ")
    rlist, _, _ = select.select([sys.stdin], [], [], 1)
    if rlist:
        input = sys.stdin.readline().strip().lower()
        processManualInput(input)
def processManualInput(input):
    if input == 'k':
        activateFailsafe()
    elif len(input)>4 and input[0:4].lower()=='pan ':
        handlePan(input)
    elif len(input)>5 and input[0:5].lower()=='tilt ':
        handleTilt(input)
def handlePan(command):
    deltaAngle=0
    try:
        deltaAngle = float(command.split(" ")[1])
    except ValueError:
        print("input a number goofy ahh individual")
    pan(deltaAngle)
def handleTilt(command):
    deltaAngle=0
    try:
        deltaAngle = float(command.split(" ")[1])
    except ValueError:
        print("input a number goofy ahh individual")
    tilt(deltaAngle)
    print('tilted '+str(deltaAngle))
def pan(delta):
    curPan=servoPan.swivel(delta)
    dummyPan.swivel(delta*-1)
    print(f'Panned: {delta}. Pan angle: {curPan}')
def tilt(delta):
    curTilt=servoTilt.swivel(delta)
    #dummyTilt.swivel(delta*-1)
    print(f'Tilted: {delta}. Tilt angle: {curTilt}')

calibrate=input("Calibrate? (y/n): ")
if(calibrate.lower()=='y'):
    successCount=0
    while successCount<listAverageSize:
        success= processData()
        if success:
            successCount+=1
        sys.stdout.write(f"\r{curListIndex+1}/{listAverageSize}")
print()
LAT_MIN=sum(latList)/listAverageSize-latVariance
LAT_MAX=sum(latList)/listAverageSize+latVariance
LONG_MIN=sum(longList)/listAverageSize-longVariance
LONG_MAX=sum(longList)/listAverageSize+longVariance
ALT_MAX=sum(altList)/listAverageSize+altVariance
print(f"bounding box lat: {LAT_MIN}-{LAT_MAX} long: {LONG_MIN}-{LONG_MAX} alt: {ALT_MAX}")

start_time = time.time()
cur_time = start_time
last_cam_capture = start_time
itr = 0

while(True):
    processData()
    if(not (LAT_MIN<sum(latList)/listAverageSize<LAT_MAX) or not (LONG_MIN<sum(longList)/listAverageSize<LONG_MAX) or sum(altList)/listAverageSize>ALT_MAX):
        initFailsafeCountdown()
        failsafeCountdown(time.time())
    manualControls()
    cur_time = time.time()
    if last_cam_capture + DELAY_CAM_CAPTURE < cur_time:
        cam.capture_image(False, itr)
        last_cam_capture = cur_time
        itr += 1
