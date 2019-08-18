import config as thmr_config
from registry.schema import User, Patient, Hospital, Surgery, Episode, EpisodeType
from registry.tests import names


def test_data_generate(database_session):
    found_users = database_session.query(User).count()
    assert found_users == thmr_config.Config.TEST_NUM_USERS
    assert database_session.query(Patient).count() == thmr_config.Config.TEST_NUM_PATIENTS

    assert database_session.query(Hospital).count() == len(names.cities)
    assert database_session.query(Episode).count() > 0
    assert database_session.query(Surgery).count() > 0

    for episode in database_session.query(Episode).all():
        assert len(episode.hospital.name) > 0
        if episode.episode_type == EpisodeType.Surgery:
            assert episode.surgery is not None
            assert episode.surgery.episode.id == episode.id
