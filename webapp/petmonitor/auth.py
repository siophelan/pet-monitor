import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from petmonitor.db import get_db

# create an 'auth' Blueprint 
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# view 1: register
@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    # if user has submitted form
    if request.method == 'POST':
        fname = request.form['floatingFN']
        lname = request.form['floatingLN']
        phone = request.form['floatingPhone']
        email = request.form['floatingEmail']
        pw = request.form['floatingPassword']
        db = get_db()
        error = None

        # validate inputs
        if not fname:
            error = 'You must provide a first name.'
        elif not lname:
            error = 'You must provide a last name.'
        elif not phone:
            error = 'You must provide a phone number.'
        elif not email:
            error = 'You must provide an email address.'
        elif not pw:
            error = 'You must provide a password.'
        
        if error is None:
            try:
                # execute INSERT sql statement and securely hash password
                db.execute(
                    "INSERT INTO caregiver (first_name, last_name, phone_num, email_address, password_hash) VALUES (?, ?, ?, ?, ?)",
                    (fname, lname, phone, email, generate_password_hash(pw)),
                )
                db.commit()

            except db.IntegrityError:
                # show error if email address already exists in database
                error = f"User {email} is already registered."
            else:
                # redirect user to login view
                return redirect(url_for('auth.login'))
        
        flash(error)
    
    return render_template('auth/register.html')


# view 2: login
@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['floatingEmail']
        pw = request.form['floatingPassword']
        db = get_db()
        error = None

        # query and store user in variable
        user = db.execute(
            'SELECT * FROM caregiver WHERE email_address = ?', (email,)
        ).fetchone()

        if user is None:
            # display error if user not in database
            error = 'Incorrect username.'
        elif not check_password_hash(user['password_hash'], pw):
            # display error if password hash check fails
            error = 'Incorrect password.'
        
        if error is None:
            # store user's id and displayname in new session
            session.clear()
            session['user_id'] = user['id']
            session['loggedin'] = user['first_name']

            # redirect user to dashboard
            return redirect(url_for('dash.dash'))
        
        flash(error)

    return render_template('auth/login.html')


# function that runs before view functions
@auth_bp.before_app_request
def load_logged_in_user():

    # read user id from session
    user_id = session.get('user_id')

    # g.user stores data for duration of request
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM caregiver WHERE id = ?', (user_id,)
        ).fetchone()


# view 3: logout
@auth_bp.route('/logout')
def logout():

    # remove the user id from the session
    session.clear()
    return redirect(url_for('index'))


# authentication wrapper for other views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):

        # redirect to login view if no user is stored
        if g.user is None:
            return redirect(url_for('auth.login'))

        # call original view and proceed as normal
        return view(**kwargs)
    
    return wrapped_view