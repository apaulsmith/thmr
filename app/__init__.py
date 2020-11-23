from distutils.util import strtobool
import logging
import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from app import formatters
from app.util import pwd_generator

db = SQLAlchemy()
login = LoginManager()

LOG_FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
LOG_DATE_FMT = '%Y-%m-%d %H:%M:%S'


def create_app(unit_test=False):
    """Initialize the core app."""

    init_logging()

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

        database_url = 'mysql+mysqlconnector://%(USER)s:%(PASSWORD)s@%(HOST)s:%(PORT)s/%(NAME)s' % DATABASE
    else:
        database_url = 'sqlite:///:memory:'

    logging.info('Initalising SQLAlchmeny with database URL {}'.format(database_url))

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or pwd_generator.password(),
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_POOL_RECYCLE=280,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=not unit_test,
        DEFAULT_TEST_ACCOUNT_LOGIN=bool(strtobool(os.environ.get('DEFAULT_TEST_ACCOUNT_LOGIN', 'False')))
    )

    # Initialize Plugins
    db.init_app(app)
    app.db = db

    # Setup the login manager
    login.init_app(app)
    login.login_view = 'login'

    # Register custom formattters
    app.jinja_env.filters['datetime'] = formatters.format_datetime

    # Set custom JSON Encode
    # app.json_encoder = CustomJSONEncoder()

    with app.app_context():
        # Include our Routes
        from . import routes
        from . import models
        from . import forms

        logging.info('Completed Flask setup for {}'.format(app))
        return app


def init_logging():
    log_level_name = os.environ.get('LOG_LEVEL', 'INFO')
    log_level = logging.getLevelName(log_level_name.upper())
    if not log_level:
        log_level = logging.INFO

    logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FMT, level=log_level)
