""" A script to control the motion capture element 
of the pet monitoring station """

from gpiozero import MotionSensor
from picamera import PiCamera
from time import sleep
from datetime import datetime, timedelta

pir = MotionSensor(17)
camera = PiCamera()
camera.rotation = 270
TIMESTAMP = ""                              # will update dynamically for filenames
interval = timedelta(seconds=30)            # minimum time between captures
program_duration = timedelta(minutes=30)    # time that program should run for

def main():
    
    print("-----Entering motion capture mode-----")
    print("CTRL+C to end")
    start_time = datetime.now() # program start time

    sleep(5) # slight delay allows tester to change position

    # outer while loop should execute once only
    while True:

        # start monitoring
        pir.wait_for_motion()

        # first activity detected
        point_in_time = datetime.now()
        print("Movement detected at " + point_in_time.strftime("%H:%M:%S"))
        camera.start_preview()
        sleep(2)
        take_photo()
        update_log()
        record_video()
        
        # inner while loop executed until completion
        while True:

            # continue to monitor
            pir.wait_for_motion()

            # new activity detected
            new_point_in_time = datetime.now()
            print("Movement detected at " + new_point_in_time.strftime("%H:%M:%S"))
            
            # sufficient time (see interval) elapsed since last recorded activity
            if (new_point_in_time - point_in_time) >= interval:

                # log new activity
                take_photo()
                update_log()
                record_video()

                # reset original point_in_time to latest recorded activity
                point_in_time = new_point_in_time

                # return to start of inner while loop
            
            else:
                print("Still monitoring...")
                
                # return to start of inner while loop

            sleep(1)    # program sleeps to reduce load on CPU

            #pir.wait_for_no_motion() # replaced with loop below

            # conditions for program end
            if (datetime.now() - start_time) >= program_duration:
                camera.stop_preview()
            
# function to capture still image
def take_photo():
    global TIMESTAMP
    TIMESTAMP = datetime.now().strftime("%y%m%d_%H%M%S")
    camera.capture("/home/sio/myssd/petmonitor/images/img_{timestamp}.jpg".format(timestamp=TIMESTAMP))
    print("Photo taken!")

# function to capture 10-second video
def record_video():
    global TIMESTAMP
    TIMESTAMP = datetime.now().strftime("%y%m%d_%H%M%S")
    camera.start_recording("/home/sio/myssd/petmonitor/videos/vid_{timestamp}.h264".format(timestamp=TIMESTAMP))
    sleep(10)   # record for 10 seconds
    camera.stop_recording()
    print("Video recorded!")

# placeholder function to log the activity
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
