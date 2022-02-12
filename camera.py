# A script to control the camera module

from picamera import PiCamera
from time import sleep

camera = PiCamera()

# function to capture still image and save to file with sequential numbering
def takephoto():
    image = 1               # set file count to 1
    camera.start_preview()  # start preview mode to adjust to light settings
    sleep(3)                # wait 3 seconds
    camera.capture(
        '/home/sio/testimages/Catcam/test%03d.jpg' % image)  # take photo; save to file path
    image += 1              # increment file count
    camera.stop_preview()   # end preview mode


# function to capture 10-second video and save to file with sequential numbering
def takevideo():
    video = 1               # set file count to 1
    camera.start_preview()  # start preview mode to adjust to light settings
    camera.start_recording(
        '/home/sio/testvideos/Catcam/test%03d.h264' % video)  # begin video capture; save to file path
    sleep(10)               # wait 10 seconds
    camera.stop_recording() # stop video capture
    video += 1              # increment file count
    camera.stop_preview()   # end preview mode


# test functionality
camera.takephoto()
camera.takephoto()
camera.takephoto()

camera.takevideo()
camera.takevideo()