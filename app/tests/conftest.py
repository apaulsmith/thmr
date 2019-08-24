import pytest

from app import create_app
from app.tests import data_generator

TEST_NUM_USERS = 12
TEST_NUM_PATIENTS = 50


@pytest.fixture(scope="module")
def database_session():
    application = create_app()

    with application.app_context():
        application.db.create_all()
        data_generator.create_sample_data(application.db.session,
                                          num_users=TEST_NUM_USERS,
                                          num_patients=TEST_NUM_PATIENTS)

        yield application.db.session

        application.db.session.close()
        application.db.drop_all()
