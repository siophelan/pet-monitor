import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from datetime import datetime

from petmonitor.auth import login_required
from petmonitor.dash import get_pets
from petmonitor.db import get_db

# create a 'profile' Blueprint
profile_bp = Blueprint('profile', __name__)


# view 1: update profile
@profile_bp.route('/update', methods=('GET', 'POST'))
@login_required
def update():

    user_id = session.get('user_id')

    # if user has submitted form
    if request.method == 'POST':
        
        phone = request.form['inputPhone']
        email = request.form['inputEmail']
        pw = request.form['inputPassword']
        error = None
        confirmation = None

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

            # show confirmation message
            confirmation = "Profile updated!"
            flash(confirmation)

            return redirect(url_for('profile.update'))
    
    # regardless of form submission
    now = datetime.now()
    today_string = now.strftime("%A, %d %B %Y")
    profile = get_profile(user_id)

    # variables to send to client-side
    view_variables = {
        'date' : today_string,
        'profile' : profile
    }

    return render_template('profile/update.html', **view_variables)


# view 2: add a pet
@profile_bp.route('/addpet', methods=('GET', 'POST'))
@login_required
def addpet():

    user_id = session.get('user_id')

    # if user has submitted form
    if request.method == 'POST':
        p_name = request.form['floatingPetName']

        if request.form['floatingSpecies'] == "Cat":
            p_species = 1
        else:
            p_species = 2
            
        if request.form['floatingYear'] is not None:
            year = request.form['floatingYear']
            sql = "INSERT INTO pet (pet_name, birth_year, species_ID) VALUES (?, ?, ?)"
            val = (p_name, year, p_species)
        else:
            sql = "INSERT INTO pet (pet_name, species_ID) VALUES (?, ?)"
            val = (p_name, p_species)
        
        error = None
        confirmation = None

        # validate inputs
        if not p_name:
            error = 'You must provide a pet name.'
        elif not p_species:
            error = 'You must confirm the species.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(sql, val)
            db.commit()
            
            # get  ID for last created record in pet, save as variable
            pet = db.execute(
            'SELECT * FROM pet ORDER BY id DESC'
            ).fetchone()
            pet_id = pet['id']
                
            db.execute(
                "INSERT INTO pet_caregiver (pet_id, caregiver_id) VALUES (?, ?)",
                (pet_id, user_id), 
            )
            db.commit()

            # show confirmation message
            confirmation = "Pet added!"
            flash(confirmation)

            return redirect(url_for('profile.update'))
        



    # regardless of form submission
    now = datetime.now()
    pets = get_pets(user_id)
    curr_year = now.strftime("%Y")

    # variables to send to client-side
    view_variables = {
        'pets' : pets,
        'currYear' : curr_year
    }

    return render_template('profile/addpet.html', **view_variables)


# function to retrieve a user profile
def get_profile(id):

    profile = get_db().execute(
        'SELECT caregiver.id, caregiver.first_name, caregiver.last_name, caregiver.phone_num,' 
        ' caregiver.email_address FROM caregiver'
        ' WHERE caregiver.id = ?',
        (id,)
    ).fetchone()

    if profile is None:
        abort(404, f"Profile for user {id} does not exist") 
    
    if profile['id'] != g.user['id']:
        abort(403)

    return profile