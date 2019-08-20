import logging
import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.INFO)

application = Flask(__name__)

# _application.json_encoder = CustomJSONEncoder
# _application.json_decoder = CustomJSONDecoder

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
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    database_url = 'sqlite:///:memory:'
    # database_url = 'sqlite:///' + os.path.join(BASE_PATH, 'database', 'registry.sqlite')

application.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-guess',
    SQLALCHEMY_DATABASE_URI=database_url,
    SQLALCHEMY_POOL_RECYCLE=280,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Setup the login manager
login = LoginManager(application)
login.login_view = 'login'

db = SQLAlchemy(app=application)

import app.routes
