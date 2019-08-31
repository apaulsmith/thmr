import pytest

from app import create_app
from app.tests import data_generator

TEST_NUM_USERS = 12
TEST_NUM_PATIENTS = 50


@pytest.fixture(scope="class")
def flask_application():
    application = create_app(unit_test=True)

    with application.app_context():
        application.db.create_all()
        data_generator.create_sample_data(application.db.session,
                                          num_users=TEST_NUM_USERS,
                                          num_patients=TEST_NUM_PATIENTS)

        yield application

        application.db.session.close()
        application.db.drop_all()


@pytest.fixture(scope="class")
def database_session(flask_application):
    with flask_application.app_context():
        yield flask_application.db.session


@pytest.fixture(scope="function")
def flask_client(flask_application):
    with flask_application.app_context():
        yield flask_application.test_client()
