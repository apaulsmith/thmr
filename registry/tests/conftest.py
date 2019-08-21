import pytest

from app import create_app
from registry.tests import data_generator


@pytest.fixture(scope="module")
def database_session():
    application = create_app()

    with application.app_context():
        application.db.create_all()
        data_generator.create_sample_data(application.db.session,
                                          num_users=12,
                                          num_patients=50)

        yield application.db.session

        application.db.session.close()
        application.db.drop_all()
