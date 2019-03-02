import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DB_URL = 'sqlite:///' + os.path.join(BASE_PATH, 'database', 'registry.sqlite')

# Enable Flask's debugging features. Should be False in production
DEBUG = True
