# A script to control the motion capture component of the pet monitoring station

from gpiozero import MotionSensor
from picamera import PiCamera
from time import sleep, strftime, gmtime
from datetime import datetime, timedelta

pir = MotionSensor(17)
camera = PiCamera()
camera.hflip = True

def main():
    print("### Testing motion capture (enter CTRL+C to end) ###")

    while True:
        pir.wait_for_motion()

        # on signal from PIR sensor
        movement_time = gmtime()
        print("Movement detected at " + strftime(
            "%H:%M:%S", movement_time) + "!")
        camera.start_preview()        

        # file storage settings
        global imgfilepath, vidfilepath
        timestamp = strftime("%y%m%d_%H%M%S", movement_time)
        imgfilepath = (
            "/home/sio/myssd/petmonitor/images/img_{timestamp}.jpg".format(timestamp=timestamp))
        vidfilepath = (
            "/home/sio/myssd/petmonitor/videos/vid_{timestamp}.h264".format(timestamp=timestamp))
        
        # first pass
        take_photo()
        record_video()
        
        # subsequent passes
        #prev_move = movement_time
        #new_move = datetime.now()
        #five_mins = timedelta(minutes=5)
        #thirty_secs = timedelta(seconds=30) # TEST ONLY

        # establish time between timestamps
        #if (new_move - prev_move) > thirty_secs:
            #print("Over 30 seconds have passed!")
            #timestamp = strftime("%y%m%d_%H%M%S", new_move)
            #take_photo()
            #record_video()
        #else:
            # continue to monitor for movement
            #print("Still monitoring...")

        pir.wait_for_no_motion()
        camera.stop_preview()

# function to capture still image with timestamped filename
def take_photo():
    sleep(2)    # 2 second delay
    camera.capture(imgfilepath)
    print("Photo taken!")
    # create database entry

# function to capture 10-second video with timestamped filename
def record_video():
    camera.start_recording(vidfilepath)
    sleep(10)   # record for 10 seconds
    camera.stop_recording()
    print("Video recorded!")
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