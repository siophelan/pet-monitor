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
        global imgfilepath, vidfilepath
        timestamp = strftime("%y%m%d_%H%M%S", gmtime())
        imgfilepath = (
            "/home/sio/Catcam/testimages/img_{timestamp}.jpg".format(timestamp=timestamp))
        vidfilepath = (
            "/home/sio/Catcam/testvideos/vid_{timestamp}.h264".format(timestamp=timestamp))
        
        # STILL TO FIGURE OUT:
        # if time elapsed between timestamps is > 5 mins, then:
        # take photo and record video
        # else continue

        take_photo()
        
        record_video()

        pir.wait_for_no_motion()
        camera.stop_preview()

# function to capture still image with timestamped filename
def take_photo():
    sleep(2)    # 2 second delay
    camera.capture(imgfilepath)
    print("Photo taken!")

# function to capture 10-second video with timestamped filename
def record_video():
    camera.start_recording(vidfilepath)
    sleep(10)   # 10 second clip
    camera.stop_recording()
    print("Video recorded!")

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