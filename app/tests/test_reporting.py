from app import reporting
from app.models import Patient, Episode


def test_patients(database_session):
    users = database_session.query(Patient).all()
    df = reporting.patients_as_df(users)

    assert len(df) == len(users)


def test_episodes(database_session):
    episodes = database_session.query(Episode).all()
    df = reporting.episodes_as_df(episodes)

    assert len(df) == len(episodes)
