from picamera2 import Picamera2
import time
import cv2

# note run as pythyon testCamera.py 2> /dev/null to supress warnings

t1 = time.time()
picam2 = Picamera2()    # use default 640x480 configuration
picam2.start()

t2 = time.time()

picam2.capture_file("test.png")
t3 = time.time()

array = picam2.capture_array("main")
t4 = time.time()

array_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
cv2.imwrite('test2.png', array_bgr)
t5 = time.time()

picam2.stop()

camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
picam2.configure(camera_config)
picam2.start()

t6 = time.time()

picam2.capture_file("test3.png")
t7 = time.time()

array = picam2.capture_array("main")
t8 = time.time()

array_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
cv2.imwrite('test4.png', array_bgr)
t9 = time.time()

picam2.stop()

print (f'Set up object and configure camera: {t2-t1:1.3f}')
print (f'Take image and save to drive: {t3-t2:1.3f}')
print (f'Take image and load into memeory: {t4-t3:1.3f}')
print (f'Save image from memory with opencv: {t5-t4:1.3f}')
print (f'Stop and reconfigure camera for higher resolution: {t6-t5:1.3f}')
print (f'Take higher resolution image and save to drive: {t7-t6:1.3f}')
print (f'Take higher resolution image and load into memory: {t8-t7:1.3f}')
print (f'Save higher resolution image from memory with opencv: {t9-t8:1.3f}')