import random
import time
import sys
import select
from gps import GPSController
from servo import Servo
from constants import PIN_SERVO_MAJOR,PIN_SERVO_MINOR, SERVO_MAX_DUTY, SERVO_MIN_DUTY

COUNTDOWN_SECONDS=15
listAverageSize=10
curListIndex=0
latList = [0]*listAverageSize
longList = [0]*listAverageSize
altList = [0]*listAverageSize
servoPan = Servo(PIN_SERVO_MAJOR, (SERVO_MAX_DUTY + SERVO_MIN_DUTY)/2)
servoTilt = Servo(PIN_SERVO_MINOR, (SERVO_MAX_DUTY + SERVO_MIN_DUTY)/2)

# TEMP: TESTING SERVO FUNCTION
time.sleep(0.05)
servoPan.swivel(5)
time.sleep(0.05)
servoPan.swivel(-5)
time.sleep(0.05)
# END TEST

latVariance=0.01
longVariance=0.01
GPS= GPSController()
def getPositionData():
    return GPS.data_snapshot()
def activateFailsafe():
    #switch pin to on
    print()
    print("  _|        _)  |                _|       ")
    print(" |     _` |  |  |   __|   _` |  |     _ \\ ")
    print(" _|   (   |  |  | \__ \\  (   |  _|    __/ ")
    print("_|   \\__._| _| _| ____/ \\__._| _|   \\___|")
for i in range(listAverageSize):
    while(True):
        lat,long,alt = getPositionData()
        if lat is not None:
            latList[i]=lat
            longList[i]=long
            altList[i]=alt
            print(f"{i+1}/{listAverageSize}")
            break
LAT_MIN=sum(latList)/listAverageSize-latVariance
LAT_MAX=sum(latList)/listAverageSize+latVariance
LONG_MIN=sum(latList)/listAverageSize-longVariance
LONG_MAX=sum(latList)/listAverageSize+longVariance
ALT_MAX=150
print(f"bounding box lat: {LAT_MIN}-{LAT_MAX} long: {LONG_MIN}-{LONG_MAX} alt: {ALT_MAX}")

while(True):
    lat,long,alt = getPositionData()
    if lat is not None:
        curListIndex+=1
        if(curListIndex>=listAverageSize):
            curListIndex=0
        latList[curListIndex]=lat
        longList[curListIndex]=long
        altList[curListIndex]=alt
    if(not (LAT_MIN<sum(latList)/listAverageSize<LAT_MAX) or not (LONG_MIN<sum(longList)/listAverageSize<LONG_MAX) or sum(altList)/listAverageSize>ALT_MAX):
        print()
        print("\\ \\        /     \\      _ \\   \\  |_ _|  \\  |  ___|")
        print(" \\ \\  \\   /     _ \\    |   |   \\ |  |    \\ | |  _  ")
        print("  \\ \\  \\ /     ___ \\   __ <  |\\  |  |  |\\  | |   |")
        print("   \\_/\\_/    _/    _\\ _| \\_\\_| \\_|___|_| \\_|\\____")
        print(f"averaged lat: {sum(latList)/listAverageSize} averaged long: {sum(longList)/listAverageSize} averaged alt: {sum(altList)/listAverageSize}")
        start_time = time.time()
        sys.stdout.write("Enter 'stop' to halt the countdown: ")
        sys.stdout.flush()
        while True:
            elapsed_time = time.time() - start_time
            remaining_time = int(COUNTDOWN_SECONDS - elapsed_time)
            if remaining_time <= 0:
                activateFailsafe()
                break
            
            sys.stdout.write(f"\rEnter 'c' to abort: {remaining_time} seconds remaining: ")
            sys.stdout.flush()
            
            rlist, _, _ = select.select([sys.stdin], [], [], 1)
            if rlist:
                input_line = sys.stdin.readline().strip()
                if input_line.lower() == 'c':
                    print("Failsafe Aborted")
                    break
    
    sys.stdout.write(f"\rEnter 'k' to manually activate failsafe, 'pan/tilt <degrees>' to pan/tilt: ")
    rlist, _, _ = select.select([sys.stdin], [], [], 1)
    if rlist:
        input = sys.stdin.readline().strip().lower()
        if input == 'k':
            activateFailsafe()
        elif len(input)>4 and input[0:4].lower()=='pan ':
            deltaAngle=0
            try:
                deltaAngle = float(input.split(" ")[1])
            except ValueError:
                print("input a number goofy ahh individual")
                continue
            servoPan.swivel(deltaAngle)
            print('panned '+str(deltaAngle))
        elif len(input)>5 and input[0:5].lower()=='tilt ':
            deltaAngle=0
            try:
                deltaAngle = float(input.split(" ")[1])
            except ValueError:
                print("input a number goofy ahh individual")
                continue
            servoTilt.swivel(deltaAngle)
            print('tilted '+str(deltaAngle))
        #match input.lower():
         #   case 'k':
          #      activateFailsafe()
           # case 'g':
            #    #feijioef
             #   print("doing gimbal things")
            #case _:
              #  print("invalid input")
    #time.sleep(.2)
