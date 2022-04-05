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
# @login_required   # Uncomment before going live!!
def dash():
    
    user_id = session.get('user_id')
    now = datetime.now()
    todayString = now.strftime("%A, %d %B %Y")
    
    loggedin = session.get('loggedin')
    if loggedin is None:
        displayname = "User"
    else:
        displayname = loggedin
    
    petList = getPets(user_id)

    # variables to send to client-side
    bpVariables = {
        'date' : todayString,
        'displayname' : displayname,
        'pets' : petList
    }

    return render_template('dash.html', **bpVariables)


# view 2: photos
@dash_bp.route('/photos', methods=('GET', 'POST'))
# @login_required   # Uncomment before going live!!
def photos():
    # db = get_db()
    # pull in stored images based on SQL query for set date range
    # range 1: today
    # range 2: last 3 days
    # range 3: this week
    # range 4: this month

    return render_template('dash/photos.html')


# view 3: videos
@dash_bp.route('/videos', methods=('GET', 'POST'))
# @login_required   # Uncomment before going live!!
def videos():
    # db = get_db()
    # pull in stored images based on SQL query for set date range
    # range 1: today
    # range 2: last 3 days
    # range 3: this week
    # range 4: this month

    return render_template('dash/videos.html')


# view 4: reports
@dash_bp.route('/reports', methods=('GET', 'POST'))
# @login_required   # Uncomment before going live!!
def reports():
    # db = get_db()
    # pull in data based on SQL query for set date range
    # range 1: today
    # range 2: last 3 days
    # range 3: this week
    # range 4: this month

    return render_template('dash/reports.html')


# function to retrieve a pet
def getPets(id):

    pets = get_db().execute(
        'SELECT caregiver.id, pet.pet_name, species.species_type, strftime("%Y", date()) - pet.birth_year as age FROM caregiver'
        ' JOIN pet_caregiver ON caregiver.id = pet_caregiver.caregiver_id'
        ' JOIN pet ON pet.id = pet_caregiver.pet_id'
        ' JOIN species ON species.id = pet.species_ID'
        ' WHERE caregiver.id = ?',
        (id,)
    ).fetchall()

    if pets is None:
        return None 

    return pets

