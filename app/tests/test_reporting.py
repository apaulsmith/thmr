from builtins import len

from app import reporting
from app.models import Patient, Episode


def test_patients(database_session):
    users = database_session.query(Patient).all()
    d = reporting.patients_as_dict(users)

    for k, v in d.items():
        assert len(v) == len(users)


def test_episodes(database_session):
    episodes = database_session.query(Episode).all()
    d = reporting.episodes_as_dict(episodes)

    for k, v in d.items():
        assert len(v) == len(episodes)
