import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.exceptions import abort

from datetime import datetime

from petmonitor.auth import login_required
from petmonitor.db import get_db

# create a 'dash' Blueprint
dash_bp = Blueprint('dash', __name__)


# view 1: dashboard
@dash_bp.route('/dash', methods=('GET', 'POST'))
@login_required
def dash():
    
    user_id = session.get('user_id')
    now = datetime.now()
    today_string = now.strftime("%A, %d %B %Y")
    curr_year = int(now.strftime("%Y"))

    # select a random image from capture log in database
    sql = "SELECT img_timestamp from photo ORDER BY RANDOM() LIMIT 1"
    db = get_db()
    random_image = "img_" + dict(db.execute(sql).fetchone())['img_timestamp'] + ".jpg"
    image = url_for('static', filename="captures/images/{random_image}".format(random_image=random_image))
    
    loggedin = session.get('loggedin')
    if loggedin is None:
        displayname = "User"
    else:
        displayname = loggedin
    
    pet_list = get_pets(user_id)

    # variables to send to client-side
    view_variables = {
        'date' : today_string,
        'yearNotAge' : curr_year,
        'displayname' : displayname,
        'pets' : pet_list,
        'image' : image
    }

    return render_template('dash.html', **view_variables)


# view 2: photos
@dash_bp.route('/photos', methods=('GET', 'POST'))
@login_required
def photos():

    filetype = "img"
    date_range = "month"    # hardcoded for testing purposes only, should read from user input
    img_list = get_filenames(filetype, date_range)  
    
    return render_template('dash/photos.html', img_list=img_list)


# view 3: videos
@dash_bp.route('/videos', methods=('GET', 'POST'))
@login_required
def videos():
    
    filetype = "vid"
    date_range = "month"    # hardcoded for testing purposes only, should read from user input
    vid_list = get_filenames(filetype, date_range)

    return render_template('dash/videos.html', vid_list=vid_list)


# view 4: reports
@dash_bp.route('/reports', methods=('GET', 'POST'))
@login_required
def reports():
    # db = get_db()
    # pull in data based on SQL query for set date range
    # range 1: today... sql = "SELECT * from activity WHERE activity_date IS date('now')"
    # range 2: last 3 days... sql = "SELECT * from activity WHERE activity_date > date('now', '-3 day')"
    # range 3: this week... sql = "SELECT * from activity WHERE activity_date > date('now', '-7 day')"
    # range 4: this month... sql = "SELECT * from activity WHERE activity_date > date('now', '-1 month')"

    sql = "SELECT * from activity WHERE activity_date > date('now', '-3 day')"
    db = get_db()
    raw_data = db.execute(sql).fetchall()

    print([dict(row)['activity_date'] for row in raw_data])

    #data_points = 
    # [{ x : ['2022-04-17', '2022-04-18'], y : [4, 1], type: 'bar' }];


    return render_template('dash/reports.html')


# function to retrieve a pet
def get_pets(id):

    pets = get_db().execute(
        'SELECT caregiver.id, pet.id as pet_id, pet.pet_name, species.species_type, strftime("%Y", date()) - pet.birth_year as age FROM caregiver'
        ' JOIN pet_caregiver ON caregiver.id = pet_caregiver.caregiver_id'
        ' JOIN pet ON pet.id = pet_caregiver.pet_id'
        ' JOIN species ON species.id = pet.species_ID'
        ' WHERE caregiver.id = ?',
        (id,)
    ).fetchall()

    if pets is None:
        return None 

    return pets


# function to retrieve a list of filenames
def get_filenames(filetype, date_range):

    # use filetype to determine table to query
    if (filetype=="img"):
        db_table = "photo"
    elif (filetype=="vid"):
        db_table = "video"

    # use date_range to customise SQL statement
    if (date_range=="today"):
        search_range = "IS date('now')"
    elif (date_range=="threeday"):
        search_range = "> date('now', '-3 day')"
    elif (date_range=="week"):
        search_range = "> date('now', '-7 day')"
    elif (date_range=="month"):
        search_range = "> date('now', '-1 month')"
    else:
        # default date range is today
        search_range = "IS date('now')"
        
    sql = "SELECT {filetype}_timestamp from {db_table} WHERE {filetype}_date {search_range}".format(filetype=filetype, db_table=db_table, search_range=search_range)

    raw_data = get_db().execute(sql).fetchall()
    # print([dict(row)['img_timestamp'] for row in raw_data])   # testing only
    timestamp_list = [dict(row)['{filetype}_timestamp'.format(filetype=filetype)] for row in raw_data]

    if timestamp_list is None:
        return None
    
    return timestamp_list