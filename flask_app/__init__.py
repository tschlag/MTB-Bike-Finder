import os
from flask import Flask

def create_app(test_config=None):
    # Creates the flask app and specifies the DB
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask_app.sqlite'),
    )

    # Sets up the instance folder if not already created
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initializes the Flask app, registers both blueprints
    from . import db, auth, main_page
    db.init_app(app)

    app.register_blueprint(auth.bp)

    app.register_blueprint(main_page.bp)
    app.add_url_rule('/', endpoint='index')

    return app