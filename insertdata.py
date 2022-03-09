# A script to update an SQLite database file

import sqlite3
from sqlite3 import Error
from datetime import datetime

def connect_to_DB(db_file):
    
    conn = None

    try:
        conn = sqlite3.connect(db_file)

    except Error as e:
        print(e)
    
    return conn

def add_record(conn, data):

    # syntax for SQL query
    #sql = '''INSERT INTO user(name, email, password) VALUES(?,?,?)'''
    sql = '''INSERT INTO activity(date, time, last_activity) VALUES(?,?,?)'''

    #create a cursor object
    cur = conn.cursor()

    # execute the query
    cur.execute(sql, data)

    # commit the changes
    conn.commit()

    # return the ID of the newly-created record
    return cur.lastrowid

def add_user():
    print("---Add a new user---")
    # get values from user input
    print("Name: ", end = "")
    un = input()
    print("Email: ", end ="")
    email = input()
    print("Password: ", end = "")
    pw = input()
    return un, email, pw

def add_activity():
    print("---Add new activity---")
    # get values from system clock
    date_now = datetime.now().strftime("%y-%m-%d")
    time_now = datetime.now().strftime("%H:%M:%S")
    last_log = ""
    return date_now, time_now, last_log

def get_last_activity():
    # continue working out tomorrow
    #sql = '''SELECT FROM '''
    pass

def main():
    database = r"/home/sio/catcam/testdatabase.db"

    # add a new user
    #user_name, user_email, user_password = add_user()

    # add activity data
    curr_date, curr_time, prev_log = add_activity()

    # create database connection
    conn = connect_to_DB(database)
    with conn:

        # values for new user
        #new_user = (user_name, user_email, user_password)
        #user_id = add_record(conn, new_user)
        #print("New user added to database: record #", user_id)

        # values for new activity
        new_activity = (curr_date, curr_time, prev_log)
        activity_id = add_record(conn, new_activity)
        print("New activity added to database: record #", activity_id)

# execute the code
if __name__ == '__main__':
    main()
