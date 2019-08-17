import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DB_URL = 'sqlite:///' + os.path.join(BASE_PATH, 'database', 'registry.sqlite')
DB_TEST_URL = 'sqlite:///:memory:'

# Test-case configuration
TEST_NUM_USERS = 12
TEST_NUM_PATIENTS = 50
TEST_NUM_SURGERIES = 50

# Enable Flask's debugging features. Should be False in production
DEBUG = True
