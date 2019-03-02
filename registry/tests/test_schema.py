import config
from registry import schema


def test_tables():
    metadata = schema.build_schema_metadata()

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


def test_create_engine():
    engine = schema.create_engine()

    assert engine
    assert config.DB_URL in str(engine)


def test_create_engine_singleton():
    engine = schema.create_engine()
    engine2 = schema.create_engine()
    engine3 = schema.create_engine()

    assert engine is engine2
    assert engine2 is engine3
