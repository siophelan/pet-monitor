# A script to control the PIR sensor

import RPi.GPIO as GPIO

# suppress warnings from the library
GPIO.setwarnings (False) 

# configure the pins
GPIO.setmode(GPIO.BOARD)

# configure pins 4 (power), 6 (ground) and 11 (output) using following syntax:
# GPIO.setup(pin_number, GPIO.IN/ GPIO.OUT)

# set a pullup or pulldown resistor for input pins using following syntax:
# GPIO.setup(pin_number, GPIO,IN, pull_up_donw=GPIO.PUD_UP)

# turn pins on using following syntax:
# GPIO.output(pin_number, True)

# or off using following syntax:
# GPIO.output(pin_number, False)

try:
    # WHILE motion detected (True):
        # IF sensor signal received:
            print('Motion detected!')
        # ELSE:
            # DO SOMETHING ELSE
            print('No motion detected...')

except KeyboardInterrupt:
    # if program interrupted by CTRL+C key press
    # DO SOMETHING BEFORE PROGRAM EXITS

except:
    # for all other errors
    print('Error or exception occurred!')

finally:
    # clean up any GPIO ports used on program exit
    GPIO.cleanup()