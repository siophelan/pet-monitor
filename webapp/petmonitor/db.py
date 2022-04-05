import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    # g points to the Flask application handling the request
    if 'db' not in g:
        g.db = sqlite3.connect(
            # establish connection to file in DATABASE config key
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # allow access to columns by name
        g.db.row_factory = sqlite3.Row
    
    return g.db


def close_db(e=None):
    # check whether g.db was set (i.e. if connection was created)
    db = g.pop('db', None)

    # if connection exists, close it
    if db is not None:
        db.close()


def init_db():
    # return the database connection
    db = get_db()

    # open file relative to the petmonitor package
    with current_app.open_resource('schema.sql') as file:
        # execute SQL commands
        db.executescript(file.read().decode('utf8'))


# define a command-line command to initialise the database
@click.command('init-db')
@with_appcontext
def init_db_command():
    # clear the existing data and create new tables
    init_db()
    click.echo('Initialised the database.')


# register the close_db and init_db_command functions with the app instance
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
