import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

    # DB_URL = 'sqlite:///' + os.path.join(BASE_PATH, 'database', 'registry.sqlite')
    DB_URL = 'mysql+mysqlconnector://thmr:39rq6E2HaG3W7n6QJ48B@thmr-test-ldn-instance-1.cjtuf2egyhbw.eu-west-2.rds.amazonaws.com/thmr'
    DB_TEST_URL = 'sqlite:///:memory:'

    # Test-case configuration
    TEST_NUM_USERS = 12
    TEST_NUM_PATIENTS = 50

    # Enable Flask's debugging features. Should be False in production
    DEBUG = True
