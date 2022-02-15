# A script to control the motion capture component of the pet monitoring station

from gpiozero import MotionSensor
from picamera import PiCamera
from time import sleep

pir = MotionSensor(17)
camera = PiCamera()
# optional: set camera.resolution and/or camera.framerate
# optional: configure other camera settings, e.g. camera.awb_mode; camera.exposure_mode; camera.ISO

try:
    print("Testing motion capture (enter CTRL+C to end)")

    # wait for signal from PIR sensor
    while True:
        pir.wait_for_motion()
        print("Movement detected!")
        camera.start_preview()
        pir.wait_for_no_motion()
        camera.stop_preview()

except KeyboardInterrupt:
    # if program interrupted by CTRL+C key press
    print("Test ended!")
    camera.stop_preview()

except:
    # for all other errors
    print("An error or exception occurred!")
    camera.stop_preview()

finally:
    camera.stop_preview()
    camera.close()