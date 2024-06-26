# A script to update an SQLite database file

import sqlite3
from sqlite3 import Error
from datetime import datetime

# function to connect to a database file
def connect_to_DB(db_file):

    # create and return connection
    conn = None

    try:
        conn = sqlite3.connect(db_file)

    except Error as e:
        print(e)
    
    return conn

# function to add a new record
def add_record(conn, data):

    # syntax for SQL query
    sql = '''INSERT INTO activity(activity_date, activity_time, last_activity) VALUES(?,?,?)'''

    #create a cursor object
    cur = conn.cursor()

    # execute the SQL query
    cur.execute(sql, data)

    # commit the changes
    conn.commit()

    # return the ID of the newly-created record
    return cur.lastrowid

# function to retrieve the date and time of last activity
def get_last_activity(conn):

    # create a cursor object
    cur = conn.cursor()

    # execute the SQL query
    cur.execute("SELECT activity_date, activity_time FROM activity ORDER BY id DESC")

    # get the values from the most recent record only
    prev_date, prev_time = cur.fetchone()

    # concatenate timestamp and save as string
    prev_timestamp = prev_date + " " + prev_time

    # return timestamp
    return prev_timestamp

# function to add a new activity
def add_activity(conn):
    
    # get values from system clock
    date_now = datetime.now().strftime("%Y-%m-%d")
    time_now = datetime.now().strftime("%H:%M:%S")
    
    # get value from database
    last_log = get_last_activity(conn)
    
    return date_now, time_now, last_log


def main():

    database = r"webapp\instance\petmonitor.sqlite"

    # create database connection
    conn = connect_to_DB(database)
    with conn:

        # values for new activity
        curr_date, curr_time, prev_log = add_activity(conn)
        new_activity = (curr_date, curr_time, prev_log)
        activity_id = add_record(conn, new_activity)
        print("New activity added to database: record #", activity_id)

# execute the code
if __name__ == '__main__':
    main()
