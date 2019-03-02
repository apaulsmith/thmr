from registry import schema


def test_tables():
    metadata = schema.build_schema_metadata()

    expected_tables = [
        'UserTypes', 'Users', 'Patients', 'Hospitals', 'UsersHospitals', 'Operations', 'Surgery', 'SurgeryUsers'
    ]

    for t in expected_tables:
        assert t in metadata.tables
