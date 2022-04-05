import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from datetime import datetime

from petmonitor.auth import login_required
from petmonitor.db import get_db

# create a 'profile' Blueprint
profile_bp = Blueprint('profile', __name__)


# function to retrieve a user profile
def get_profile(id):

    profile = get_db().execute(
        'SELECT caregiver.id, caregiver.first_name, caregiver.last_name, caregiver.phone_num, caregiver.email_address, pet.pet_name, pet.birth_year, species.species_type FROM caregiver'
        ' JOIN pet_caregiver ON caregiver.id = pet_caregiver.caregiver_id'
        ' JOIN pet ON pet.id = pet_caregiver.pet_id'
        ' JOIN species ON species.id = pet.species_ID'
        ' WHERE caregiver.id = ?',
        (id,)
    ).fetchone()

    if profile is None:
        abort(404, f"Profile for user {id} does not exist") 
    
    if profile['id'] != g.user['id']:
        abort(403)

    return profile

# view 1: update profile
@profile_bp.route('/update', methods=('GET', 'POST'))
@login_required
def update():

    user_id = session.get('user_id')

    # if user has submitted form
    if request.method == 'POST':
        
        phone = request.form['floatingPhone']
        email = request.form['floatingEmail']
        pw = request.form['floatingPassword']
        error = None

        # validate inputs
        if not phone:
            error = 'You must provide a phone number.'
        elif not email:
            error = 'You must provide an email address.'
        elif not pw:
            error = 'You must provide a password.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE caregiver SET phone_num = ?, email_address = ?, password_hash = ?'
                ' WHERE id = ?',
                (phone, email, generate_password_hash(pw), user_id)
            )
            db.commit()

            return redirect(url_for('dash.dash'))
    
    now = datetime.now()
    todayString = now.strftime("%A, %d %B %Y")
    profile = get_profile(user_id)

    # variables to send to client-side
    profVariables = {
        'date' : todayString,
        'profile' : profile
    }

    return render_template('profile/update.html', **profVariables)


# view 2: add a pet
