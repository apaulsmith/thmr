from flask import Flask
from flask_login import LoginManager

from config import Config

# Initialize the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

# Setup the login manager
login = LoginManager(app)
login.login_view = 'login'

# Load the views
from app import routes, models
