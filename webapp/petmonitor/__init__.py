# __init__.py
# Contains the application factory and instructs Python to treat the petmonitor directory as a package

import os

from flask import Flask, render_template, Response

from datetime import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # set secret key to securely sign session cookies; default to TestingKey if env var not found
        SECRET_KEY=os.environ.get('SECRET_KEY') or "TestingKey",
        # set save path for SQLite database file
        DATABASE=os.path.join(app.instance_path, 'petmonitor.sqlite'),
    )

    if test_config is None:
        # override the default configuration and load the instance configuration
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test configuration
        app.config.from_mapping(test_config)

    # ensure that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    

    # test pages
    @app.route('/testpage')
    def testpage():
        return 'We are live!'
    
    @app.route('/testerr')
    def testerr():
        cats = ["Lambda", "Pi"]
        one_cat = cats[2]
        return one_cat


    # landing page for app
    @app.route('/')
    def index():
        now = datetime.now()
        timeString = now.strftime("%H:%M:%S")
        todayString = now.strftime("%A, %d %B %Y")

        # variables to send to client-side
        templateVariables = {
            'time' : timeString,
            'date' : todayString
        }
        return render_template('index.html', **templateVariables)


    # error handlers
    @app.errorhandler(Exception)          
    def basic_error(err):          
        return "An error occurred: " + str(err)
    
    @app.errorhandler(404)
    def page_not_found(err):
        return render_template('/error/page_not_found.html', error=err), 404

    @app.errorhandler(500)
    def internal_server_error(err):
        return render_template('/error/500.html', error=err), 500


    # import and call init_app function
    from . import db
    db.init_app(app)


    # import and register Blueprints
    from . import auth
    app.register_blueprint(auth.auth_bp)

    from . import dash
    app.register_blueprint(dash.dash_bp)

    from . import profile
    app.register_blueprint(profile.profile_bp)


    return app
