from flask import Flask

# Creates the flask app and specifies the DB
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE='flask_app.sqlite'
)

# Initializes the Flask app, registers both blueprints
import db, auth, main_page
db.init_app(app)

app.register_blueprint(auth.bp)

app.register_blueprint(main_page.bp)
app.add_url_rule('/', endpoint='index')

if __name__ == "__main__":
    app.run(debug=True)
