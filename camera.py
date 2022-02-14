# A script to control the camera module

from picamera import PiCamera
from time import sleep

camera = PiCamera()
# optional: set camera.resolution and/or camera.framerate
# optional: configure other camera settings, e.g. camera.awb_mode; camera.exposure_mode; camera.ISO

# function to capture still image and save to file with sequential numbering
def takephoto():
    image = 1               # set file count to 1
    sleep(2)                # wait 2 seconds
    camera.capture(
        '/home/sio/Catcam/testimages/test%03d.jpg' % image)  # take photo; save to file path
    image += 1              # increment file count


# function to capture 10-second video and save to file with sequential numbering
def takevideo():
    video = 1               # set file count to 1
    camera.start_recording(
        '/home/sio/Catcam/testvideos/test%03d.h264' % video)  # begin video capture; save to file path
    sleep(5)               # wait 5 seconds
    camera.stop_recording() # stop video capture
    video += 1              # increment file count


# test functionality
try:
    camera.start_preview()  # start preview mode to adjust to light settings
    takephoto()
    sleep(3)
    takevideo()

except KeyboardInterrupt:
    camera.stop_preview()   # end preview mode
    camera.close()

except:
    camera.stop_preview()   # end preview mode
    camera.close()

finally:
    camera.stop_preview()   # end preview mode
    camera.close()