import functools
from click import confirm

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import generate_password_hash
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

    # set variables if user has submitted form
    if request.method == 'POST':
        
        phone = request.form['inputPhone']
        email = request.form['inputEmail']
        pw = request.form['inputPassword']
        conf_pw = request.form['confirmPassword']
        sql = "UPDATE caregiver SET phone_num = ?, email_address = ?, password_hash = ? WHERE id = ?"
        
        error = None
        confirmation = None

        # validate inputs
        if not phone:
            error = "You must provide a phone number."
        elif not email:
            error = "You must provide an email address."
        elif not pw:
            error = "You must provide a password."
        elif (pw != conf_pw):
            error = "Your passwords do not match. Please try again!"
        
        if error is None:
            try:
                val = (phone, email, generate_password_hash(pw), user_id)
                
                # update database
                db = get_db()
                db.execute(sql, val)
                db.commit()

                # show confirmation message
                confirmation = "Profile updated!"
                flash(confirmation)

            except Exception as e:
                error = "An exception occurred: " + str(e)
            
            else:
                return redirect(url_for('profile.update'))

        # display errors (if present)
        flash(error)
    
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

    # set variables if user has submitted form
    if request.method == 'POST':

        p_name = request.form['floatingPetName']

        # check species type
        if request.form['floatingSpecies'] == "Cat":
            p_species = 1
        else:
            p_species = 2
        
        # adapt SQL statement depending on whether birth year has been entered
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
            error = "You must provide a pet name."
        elif not p_species:
            error = "You must confirm the species."

        if error is None:
            try:
                # update database (pet table)
                db = get_db()
                db.execute(sql, val)
                db.commit()

                # get ID for last created record in pet, save as variable
                pet = db.execute(
                'SELECT * FROM pet ORDER BY id DESC'
                ).fetchone()
                pet_id = pet['id']

                # update database (pet_caregiver table)
                db.execute(
                "INSERT INTO pet_caregiver (pet_id, caregiver_id) VALUES (?, ?)",
                (pet_id, user_id), 
                )
                db.commit()

                # show confirmation message
                confirmation = "Pet added!"
                flash(confirmation)
            
            except Exception as e:
                error = "An exception occurred: " + str(e)
            
            else:
                return redirect(url_for('profile.addpet'))
        
        # display errors (if present)
        flash(error)

    # regardless of form submission
    now = datetime.now()
    pets = get_pets(user_id)
    curr_year = now.strftime("%Y")
    year_not_age = int(curr_year)

    # variables to send to client-side
    view_variables = {
        'pets' : pets,
        'currYear' : curr_year,
        'yearNotAge' : year_not_age
    }

    return render_template('profile/addpet.html', **view_variables)


# view 3: delete a pet
@profile_bp.route('/deletepet', methods=('GET', 'POST'))
@login_required
def deletepet():

    user_id = session.get('user_id')

    # set variables if user has submitted form
    if request.method == 'POST':
        pet_to_delete = request.form['petSelect']

        error = None
        confirmation = None

        # validate inputs
        if not pet_to_delete:
            error = "No pet selected!"

        if error is None:
            try:
                first_sql = "DELETE FROM pet_caregiver WHERE pet_id = ?"
                second_sql = "DELETE FROM pet WHERE id = ?"
                val = (pet_to_delete, )

                # delete selected record from the database
                db = get_db()
                db.execute(first_sql, val)  # from pet_caregiver table
                db.execute(second_sql, val) # from pet table
                db.commit()

                # show confirmation message
                confirmation = "Pet removed from database."
                flash(confirmation)
            
            except Exception as e:
                error = "An exception occurred: " + str(e)
            
            else:
                return redirect(url_for('profile.deletepet'))
        
        # display errors (if present)
        flash(error)

    # regardless of form submission
    now = datetime.now()
    pets = get_pets(user_id)
    curr_year = now.strftime("%Y")
    year_not_age = int(curr_year)

    # variables to send to client-side
    view_variables = {
        'pets' : pets,
        'currYear' : curr_year,
        'yearNotAge' : year_not_age
    }

    return render_template('profile/deletepet.html', **view_variables)


# function to retrieve a user profile
def get_profile(id):

    profile = get_db().execute(
        'SELECT caregiver.id, caregiver.first_name, caregiver.last_name, caregiver.phone_num,' 
        ' caregiver.email_address FROM caregiver'
        ' WHERE caregiver.id = ?',
        (id,)
    ).fetchone()

    if profile is None:
        abort(404, "Profile for user {id} does not exist".format(id=id)) 
    
    if profile['id'] != g.user['id']:
        abort(403)

    return profile