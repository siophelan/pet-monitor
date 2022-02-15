# A script to test the camera module

from picamera import PiCamera
from time import sleep, gmtime, strftime

# create camera object; mirror view horizontally
camera = PiCamera()
camera.hflip = True
# optional: set camera.resolution (x, y); camera.framerate
# optional: configure other camera settings, e.g. camera.awb_mode; camera.exposure_mode; camera.ISO

# initialise filename variables as blank strings
imgfile = ""
vidfile = ""

def main():
    global imgfile
    global vidfile
    imgfile = strftime("/home/sio/Catcam/testimages/img-%y%m%d-%H%M%S.jpg", gmtime())
    vidfile = strftime("/home/sio/Catcam/testvideos/vid-%y%m%d-%H%M%S.h264", gmtime())

    camera.start_preview()  # enables camera to adjust to light settings
    take_photo()
    record_video()
    camera.stop_preview()   

# function to capture still image with timestamped filename
def take_photo():
    sleep(3)                # wait 3 seconds
    camera.capture(imgfile) # take photo and save to file path
    print("Photo taken!")

# function to capture 5-second video with timestamped filename
def record_video():
    camera.start_recording(vidfile) # begin video capture and save to file path
    sleep(5)                        # wait 5 seconds
    camera.stop_recording()         # stop video capture
    print("Video recorded!")

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("User exited camera application")
        camera.close()

    except:
        print("Error or exception occurred")
        camera.close()

    finally:
        camera.close()