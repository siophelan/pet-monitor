# A script to control the PIR sensor
from time import sleep
from datetime import datetime
from gpiozero import MotionSensor

pir = MotionSensor(17)

try:
    print("Testing PIR sensor (enter CTRL+C to end)")
    sleep(2)
    print("Ready!")

    # wait for signal from PIR sensor
    while True:
        pir.wait_for_motion()
        print("Movement detected at " + str(datetime.now()))
        sleep(5)

        pir.wait_for_no_motion()
        print("No more motion!")

except KeyboardInterrupt:
    # if program interrupted by CTRL+C key press
    print("Test ended!")

except:
    # for all other errors
    print("An error or exception occurred!")

finally:
    print("No more motion")

# note: pin state cleanup takes place at normal termination of script
# or when exceptions are handled
