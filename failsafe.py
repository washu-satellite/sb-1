import random
import time
import sys
import select
from gps import GPSController

COUNTDOWN_SECONDS=15
listAverageSize=10
LAT_MIN=0.1
LAT_MAX=2.9
LONG_MIN=0.1
LONG_MAX=2.9
ALT_MAX=2.9
curListIndex=0
latList = [(LAT_MIN+LAT_MAX)/2]*listAverageSize
longList = [(LONG_MIN+LONG_MAX)/2]*listAverageSize
altList = [ALT_MAX]*listAverageSize
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
while(True):
    lat,long,alt = getPositionData()
    if lat:
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
    sys.stdout.write(f"\rEnter 'k' to manually activate failsafe, 'g' to give gimbal commands: ")
    rlist, _, _ = select.select([sys.stdin], [], [], 1)
    if rlist:
        input = sys.stdin.readline().strip()
        match input.lower():
            case 'k':
                activateFailsafe()
            case 'g':
                #feijioef
                print("doing gimbal things")
            case _:
                print("invalid input")
    time.sleep(.2)