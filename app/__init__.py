import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Globally accessible libraries
from app.restful import CustomJSONEncoder, CustomJSONDecoder

db = SQLAlchemy()
login = LoginManager()


def create_app():
    """Initialize the core app."""
    app = Flask(__name__, instance_relative_config=False)

    if 'RDS_URL' in os.environ:
        database_url = os.environ['RDS_URL']
    elif 'RDS_HOSTNAME' in os.environ:
        DATABASE = {
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }

        database_url = ' mysql+mysqlconnector://%(USER)s:%(PASSWORD)s@%(HOST)s:%(PORT)s/%(NAME)s' % DATABASE
    else:
        database_url = 'sqlite:///:memory:'

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-guess',
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_POOL_RECYCLE=280,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Initialize Plugins
    db.init_app(app)
    app.db = db

    # Setup the login manager
    login.init_app(app)
    login.login_view = 'login'

    # Set custom JSON Encode
    # app.json_encoder = CustomJSONEncoder
    # app.json_decoder = CustomJSONDecoder

    with app.app_context():
        # Include our Routes
        from . import routes
        from . import models
        from . import forms

        return app
