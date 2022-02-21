# A script to control the motion capture component of the pet monitoring station

from gpiozero import MotionSensor
from picamera import PiCamera
from time import sleep, strftime, gmtime
from datetime import datetime, timedelta

pir = MotionSensor(17)
camera = PiCamera()
camera.rotation = 270
timestamp = ""

def main():
    
    print("-----Testing motion capture (enter CTRL+C to end)-----")

    while True:
        pir.wait_for_motion()

        # on signal from PIR sensor
        time_a = datetime.now()
        time_b = ""
        print("Movement detected at " + time_a.strftime(
            "%H:%M:%S"))
        camera.start_preview()
        sleep(2)
        
        # functions working - now need to loop
        # and incorporate timedelta check
        take_photo()
        update_log()
        record_video()
        print("Still monitoring...")
        sleep(10)
        take_photo()
        update_log()
        record_video()
        print("Still monitoring...")

        # conditions for ending program
        pir.wait_for_no_motion()
        camera.stop_preview()

# function to capture still image with timestamped filename
def take_photo():
    global timestamp
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    camera.capture("/home/sio/myssd/petmonitor/images/img_{timestamp}.jpg".format(timestamp=timestamp))
    print("Photo taken!")

# function to capture 5-second video with timestamped filename
def record_video():
    global timestamp
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    camera.start_recording("/home/sio/myssd/petmonitor/videos/vid_{timestamp}.h264".format(timestamp=timestamp))
    sleep(5)   # record for 5 seconds
    camera.stop_recording()
    print("Video recorded!")

# function to log the activity
def update_log():
    log = open("/home/sio/myssd/petmonitor/log.txt", "a")
    log_time = datetime.now().strftime("%H:%M:%S, %d-%m-%y")
    log.write("Activity logged at {timestamp}.\n".format(timestamp=log_time))
    log.close()
    print("Log updated!")

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
