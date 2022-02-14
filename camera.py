# A script to control the camera module

from picamera import PiCamera
from time import sleep

camera = PiCamera()
# optional: set camera.resolution and/or camera.framerate
# optional: configure other camera settings, e.g. camera.awb_mode; camera.exposure_mode; camera.ISO

# test basic functionality
try:
    count = 1
    camera.start_preview()
    sleep(5)                # delay to adjust to lighting
    camera.capture(
        '/home/sio/Catcam/testimages/test%03d.jpg' % count)
    count += 1
    sleep(1)
    camera.capture(
        '/home/sio/Catcam/testimages/test%03d.jpg' % count)
    count += 1
    sleep(1)
    camera.capture(
        '/home/sio/Catcam/testimages/test%03d.jpg' % count)

except KeyboardInterrupt:
    camera.stop_preview()
    print("Test cancelled!")
    camera.close()

except:
    camera.stop_preview()
    print("Error or exception occurred!")
    camera.close()

finally:
    camera.stop_preview()
    camera.close()

# FUNCTIONS STILL NEED WORK

# function to capture still image and save to file with sequential numbering
def take_photo():
    sleep(2)               
    camera.capture(
        '/home/sio/Catcam/testimages/test%03d.jpg' % count)
    count += 1

# function to capture 10-second video and save to file with sequential numbering
def take_video():
    camera.start_recording(
        '/home/sio/Catcam/testvideos/test%03d.h264' % count)
    sleep(10)              
    camera.stop_recording()
    count += 1