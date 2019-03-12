from registry.schema import Database
from registry.tests import data_generator


def test_tables():
    metadata = Database.base.metadata

    expected_tables = [
        'UserTypes',
        'Users',
        'Patients',
        'Hospitals',
        'UsersHospitals',
        'Operations',
        'Surgery',
        'SurgeryUsers'
    ]

    assert len(metadata.tables) == len(expected_tables)
    for t in expected_tables:
        assert t in metadata.tables


def test_create_database():
    Database.create_schema()
    assert True

def test_data_generate():
    Database.create_schema()

    session = Database.create_session()
    data_generator.create_sample_data(session, num_users = 10, num_patients = 50)
