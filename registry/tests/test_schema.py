from registry.schema import Database, Operations, UserType, User, Patient, Hospitals, Surgery
from registry.tests import data_generator
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


def test_create_database():
    Database.create_schema()
    assert True


def test_data_generate():
    num_users = 12
    num_patients = 50
    num_surgeries = 50

    Database.create_schema()
    session = Database.create_session()

    with session.begin_nested():
        data_generator.create_sample_data(session,
                                          num_users=num_users,
                                          num_patients=num_patients,
                                          num_surgeries=num_surgeries)

    assert session.query(UserType).count() == 3

    found_users = 0
    for user_type in session.query(UserType).all():
        count = session.query(User).filter(User.type_id == user_type.id).count()
        assert count > 0
        found_users += count

    assert num_users == found_users
    assert num_patients == session.query(Patient).count()

    assert session.query(Hospitals).count() == len(names.cities)
    assert session.query(Operations).count() == len(names.operations)

    assert session.query(Surgery).count() == num_surgeries
    surgery = session.query(Surgery).first()

    assert session.query(session.query(Operations).filter(Operations.id == surgery.operation.id).exists())
    assert session.query(session.query(Hospitals).filter(Hospitals.id == surgery.hospital.id).exists())
