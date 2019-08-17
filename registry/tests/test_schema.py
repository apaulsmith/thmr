import config as thmr_config
from registry.schema import Database, Operation, UserType, User, Patient, Hospital, Surgery
from registry.tests import names


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
        'MeshHerniaSurgery',
        'SurgeryUsers'
    ]

    assert len(metadata.tables) == len(expected_tables)
    for t in expected_tables:
        assert t in metadata.tables


def test_data_generate(database_session):
    assert database_session.query(UserType).count() == 3

    found_users = 0
    for user_type in database_session.query(UserType).all():
        count = database_session.query(User).filter(User.type_id == user_type.id).count()
        assert count > 0
        found_users += count

    assert thmr_config.TEST_NUM_USERS == found_users
    assert thmr_config.TEST_NUM_PATIENTS == database_session.query(Patient).count()

    assert database_session.query(Hospital).count() == len(names.cities)
    assert database_session.query(Operation).count() == len(names.operations)

    assert database_session.query(Surgery).count() == thmr_config.TEST_NUM_SURGERIES
    surgery = database_session.query(Surgery).first()

    assert database_session.query(
        database_session.query(Operation).filter(Operation.id == surgery.operation.id).exists())
    assert database_session.query(
        database_session.query(Hospital).filter(Hospital.id == surgery.hospital.id).exists())
