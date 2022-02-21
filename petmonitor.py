# A script to control the motion capture component of the pet monitoring station

from gpiozero import MotionSensor
from picamera import PiCamera
from time import sleep, gmtime, strftime

pir = MotionSensor(17)
camera = PiCamera()
camera.hflip = True

def main():
    print("Testing motion capture (enter CTRL+C to end)")

    while True:
        pir.wait_for_motion()

        # on signal from PIR sensor
        print("Movement detected!")
        camera.start_preview()
        
        # set variables
        global imgfilepath, vidfilepath, timestamp
        timestamp = strftime("%y%m%d_%H%M%S", gmtime())
        imgfilepath = (
            "/home/sio/catcam/testimages/img_{timestamp}.jpg".format(timestamp=timestamp))
        vidfilepath = (
            "/home/sio/catcam/testvideos/vid_{timestamp}.h264".format(timestamp=timestamp))
        
        # establish time between timestamps
        #prev_timestamp = timestamp
        #if (timestamp - prev_timestamp > 5):
            #take_photo()
            #record_video()
        # else continue to monitor for movement

        take_photo()
        
        record_video()

        pir.wait_for_no_motion()
        camera.stop_preview()

# function to capture still image with timestamped filename
def take_photo():
    sleep(2)    # 2 second delay
    camera.capture(imgfilepath)
    print("Activity detected at {timestamp}... photo taken!".format(timestamp=timestamp))
    # create database entry

# function to capture 10-second video with timestamped filename
def record_video():
    camera.start_recording(vidfilepath)
    sleep(10)   # record for 10 seconds
    camera.stop_recording()
    print("Activity detected at {timestamp}... video recorded!".format(timestamp=timestamp))
    # create database entry

# code to execute
if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        # if program interrupted by CTRL+C key press
        print("User exited program!")
        camera.close()

    except:
        # for all other errors
        print("An error or exception occurred!")
        camera.close()

    finally:
        camera.close()