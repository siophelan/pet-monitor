# A script to update a SQLite database file

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

    # pseudocode to insert a row of data, need to finetune
    sql = '''INSERT INTO activity(date("now"), time("now"), last_activity("lastrowid")) VALUES(?,?,?)'''
    
    # create a Cursor object
    cur = conn.cursor()

    # execute the query
    cur.execute(sql, data)
    
    # commit the changes
    conn.commit()
    
    # return the ID of the newly-created record
    return cur.lastrowid

def main():
    database = r"/home/sio/WDSSD/petmonitor/db/petmonitor.db"

    # create database connection
    conn = connect_to_DB(database)
    with conn:

        # pseudocode for new_record, need to finetune
        new_record = (actual_date, actual_time, actual_time_of_last_activity)
        record_id = add_record(conn, new_record)
        print("Record #: ", record_id)

# execute the code
if __name__ == '__main__':
    main()
