from registry.schema import Database


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
