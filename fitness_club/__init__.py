import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import current_user, LoginManager
from sqlalchemy import text 

db = SQLAlchemy() # initialize our database object
bcrypt = Bcrypt() # initialize our bcrypt object
login_manager = LoginManager() # initialize our login manager object
login_manager.login_view = 'auth.login'

# Create and configure an instance of the Flask application.
def create_app():
    
    app = Flask(__name__, template_folder='templates') # __name__ represents the name of file that was run. This is how you initialize flask. Also define the name of folder storing templates.
    app.config['SECRET_KEY'] = 'thisissecret' # For all flask apps, this config variable secures cookies/session data related to our website. Can be any string. In prod, wouldnt wanna share this key w/ anyone, but for this app, it's fine.

    # Database data
    username = "postgres"
    password = "56789"
    dbname = "fitness_club_project"

    # The location of our postgres database
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@localhost:5432/{dbname}" 
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app) 

    # creates an app context, within which the Flask app and its configuratoins are available for use. Useful when working with Flask components outside fo regular request/response cycle.
    with app.app_context():
        # db.create_all() will create db tables based on models, but we dont want this
        with open("fitness_club/schema.sql", 'r') as f:
            sql_commands = f.read()
        db.session.execute(text(sql_commands))
        db.session.commit()

    # import variables from files
    from .session import session
    from .dashboard import dashboard
    from .auth import users
    from .models import Member, Trainer, Admin


    # register the blueprints defined in various files. Usually urlprefix='/': if url_prefix='/auth/' and route was "hello", we must visit /auth/hello
    app.register_blueprint(session, url_prefix='/')
    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(dashboard, url_prefix='/')
    return app