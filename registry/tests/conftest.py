import pytest

from application import db
from registry.tests import data_generator


@pytest.fixture(scope="module")
def database_session():
    db.create_all()
    data_generator.create_sample_data(db.session,
                                      num_users=12,
                                      num_patients=50)

    yield db.session

    db.session.close()
    db.drop_all()
