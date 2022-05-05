""" A script to control the motion capture element of 
the pet monitoring station. The program duration and 
activity capture interval can be adjusted as required """

import sqlite3
from gpiozero import MotionSensor
from picamera import PiCamera
from sqlite3 import Error
from time import sleep
from datetime import datetime, timedelta

# ----- SETUP ------------------------------------------------------------ #

# IR sensor setup
pir = MotionSensor(17)

# camera setup
camera = PiCamera()
camera.rotation = 270                   # adjust as required for camera position

# runtime setup
interval = timedelta(seconds=30)        # minimum time between captures
program_duration = timedelta(minutes=2) # duration that program should run for

# filename timestamp, updates dynamically
save_time = ""

# database filepath
database = r"webapp\instance\petmonitor.sqlite" # possible syntax error

# ----- FUNCTIONS --------------------------------------------------------- #

# function to capture still image
def take_photo():
    global save_time
    save_time = datetime.now().strftime("%y%m%d_%H%M%S")
    #camera.capture("/home/sio/myssd/petmonitor/images/img_{timestamp}.jpg".format(timestamp=save_time))
    camera.capture(f'webapp/petmonitor/static/captures/images/img_{save_time}.jpg')
    conn = connect_to_DB(database)
    with conn:
        # log in database
        today = datetime.now().strftime("%Y-%m-%d")
        values = (today, save_time)
        create_photo_record(conn, values)
    print("Photo taken!")

# function to capture 10-second video
def record_video():
    global save_time
    save_time = datetime.now().strftime("%y%m%d_%H%M%S")
    #camera.start_recording("/home/sio/myssd/petmonitor/videos/vid_{timestamp}.h264".format(timestamp=save_time))
    camera.start_recording(f'webapp/petmonitor/static/captures/videos/vid_{save_time}.h264')
    conn = connect_to_DB(database)
    with conn:
        # log in database
        today = datetime.now().strftime("%Y-%m-%d")
        values = (today, save_time)
        create_video_record(conn, values)
    sleep(10)   # record for 10 seconds
    camera.stop_recording()
    print("Video recorded!")

# function to log the activity
def log_activity():
    conn = connect_to_DB(database)
    with conn:
        # values for new activity
        curr_date, curr_time, prev_log = get_activity_data(conn)
        new_activity = (curr_date, curr_time, prev_log)
        activity_id = create_activity_record(conn, new_activity)
        print("New activity added to database: record #", activity_id)

# function to connect to a database file
def connect_to_DB(db_file):

    # create and return connection
    conn = None

    try:
        conn = sqlite3.connect(db_file)

    except Error as e:
        print(e)
    
    return conn

# functions to create a new record
def create_activity_record(conn, data):

    # create SQL statement
    sql = '''INSERT INTO activity(activity_date, activity_time, last_activity) VALUES(?,?,?)'''

    # create a cursor object
    cur = conn.cursor()

    # execute the SQL query and commit changes
    cur.execute(sql, data)
    conn.commit()

    # return the ID of the newly-created record
    return cur.lastrowid

def create_photo_record(conn, data):

    # create SQL statement
    sql = '''INSERT INTO photo(img_date, img_timestamp) VALUES(?,?)'''

    # create a cursor object
    cur = conn.cursor()

    # execute the SQL query and commit changes
    cur.execute(sql, data)
    conn.commit()

    # return the ID of the newly-created record
    return cur.lastrowid

def create_video_record(conn, data):

    # create SQL statement
    sql = '''INSERT INTO video(vid_date, vid_timestamp) VALUES(?,?)'''

    # create a cursor object
    cur = conn.cursor()

    # execute the SQL query and commit changes
    cur.execute(sql, data)
    conn.commit()

    # return the ID of the newly-created record
    return cur.lastrowid

# function to retrieve date and time of last activity
def get_last_activity(conn):

    # create a cursor object
    cur = conn.cursor()

    # execute the SQL query
    cur.execute("SELECT activity_date, activity_time FROM activity ORDER BY id DESC")

    # fetch the most recent record only
    result = cur.fetchone()

    if result:
        prev_timestamp = result[0] + " " + result[1]    # save date and time as string
    else:
        prev_timestamp = ""

    # return timestamp
    return prev_timestamp

# function to get new activity data using established database connection
def get_activity_data(conn):
    
    # get values from system clock
    date_now = datetime.now().strftime("%Y-%m-%d")
    time_now = datetime.now().strftime("%H:%M:%S")
    
    # get value from database
    last_log = get_last_activity(conn)
    
    return date_now, time_now, last_log

# -------------------------------------------------------------------------------------------- #

def main():
    
    start_time = datetime.now()
    end_time = start_time + program_duration
    
    # console comments
    print("-----Entering motion capture mode-----")
    print(str(start_time))
    print("CTRL+C to end\n")

    sleep(5) # delay before sensor begins to monitor

    # outer loop executes once only
    while True:

        # start monitoring
        pir.wait_for_motion()

        # first activity detected
        point_in_time = datetime.now()
        print("Movement detected at " + point_in_time.strftime("%H:%M:%S"))
        
        # allow camera to adjust to light
        camera.start_preview()
        sleep(2)    

        # record activity
        print("Taking photo..")
        take_photo()
        print("Writing to DB..")
        log_activity()
        print("Starting video recording..")
        record_video()
        
        # inner loop executed for remainder of program
        while True:

            # continue to monitor
            pir.wait_for_motion()

            # new activity detected
            new_point_in_time = datetime.now()
            print("Movement detected at " + new_point_in_time.strftime("%H:%M:%S"))
            
            # sufficient time (see interval) elapsed since last recorded activity
            if (new_point_in_time - point_in_time) >= interval:

                # log new activity
                print("Taking photo..")
                take_photo()
                print("Writing to DB..")
                log_activity()
                print("Starting video recording..")
                record_video()

                # reset original point_in_time to latest recorded activity
                point_in_time = new_point_in_time
            
            else:
                print("(Activity not logged)")

            sleep(1)    # program sleeps to reduce load on CPU

            # conditions for program end
            if (datetime.now() >= end_time):
                camera.stop_preview()
                print("Program ended at " + datetime.now().strftime("%H:%M:%S"))
                return

# program code to execute
if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        # program interrupted by CTRL+C keypress
        print("User exited program!")
        camera.close()

    except Exception as e:
        # for all other errors
        print("An error or exception occurred: " + str(e))
        camera.close()

    finally:
        camera.close()
        print("Goodbye!")
