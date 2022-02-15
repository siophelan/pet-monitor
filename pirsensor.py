# A script to control the PIR sensor

from gpiozero import MotionSensor

pir = MotionSensor(17)

try:
    print("Testing PIR sensor (enter CTRL+C to end)")

    # wait for signal from PIR sensor
    while True:
        pir.wait_for_motion()
        print("Movement detected!")

except KeyboardInterrupt:
    # if program interrupted by CTRL+C key press
    print("Test ended!")

except:
    # for all other errors
    print("An error or exception occurred!")

# note: pin state cleanup takes place at normal termination of script
# or when exceptions are handled