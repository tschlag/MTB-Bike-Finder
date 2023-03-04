import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

# Connects the SQLite database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'flask_app.sqlite',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# Close the database connection if it exists
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Initializes the database and runs the schema.sql file
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# Command used in git bash to reset the database and clear out all user entered data
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# Registers the close_db and init_db_command functions with the app instance
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)