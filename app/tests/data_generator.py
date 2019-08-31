import logging
import random
from datetime import timedelta, date
from typing import List

from app import pwd_generator
from app.models import User, Patient, Hospital, Surgery, Side, Type, Cepod, Episode, EpisodeType, \
    Procedure, Complication, EpisodeAttendee
from app.tests import names

TEST_ACCOUNT_EMAIL = 'thmr_test_account@example.com'
TEST_ACCOUNT_PASSWORD = 'password'


def create_sample_data(session, num_users: int, num_patients: int):
    if session.query(User).filter(User.email == TEST_ACCOUNT_EMAIL).count() == 1:
        logging.info('Data generator has already been run in this database so skipping.')
        return
    else:
        logging.info('Running data generator.')

    users = _users(num_users)
    session.add_all(users)
    hospitals = _hospitals()
    session.add_all(hospitals)
    patients = _patients(num_patients, hospitals, users)
    session.add_all(patients)
    session.add_all(_procedures())

    for patient in patients:
        procedure = random.choice(session.query(Procedure).all())

        attendees = set()
        for i in range(0, random.randint(1, 5)):
            attendees.add(random.choice(users))

        session.add(_episode(patient, procedure, users))


def _procedures():
    return [Procedure(name='Mesh Hernia')]


def _episode(patient, procedure, users):
    episode_type = random.choice(list(EpisodeType))
    d = _date_of_surgery(1)

    if episode_type == EpisodeType.Surgery:
        surgery = _surgery(procedure)
    else:
        surgery = None

    e = Episode(
        episode_type=episode_type,
        date=d,
        patient=patient,
        hospital=patient.hospital,
        surgery=surgery,
        complications=[Complication(date=d, comments="It's complicated...")],
        created_by=random.choice(users),
        updated_by=random.choice(users),
    )

    attendees = []
    for user in users:
        attendees.append(EpisodeAttendee(
            user_id=user.id,
            episode_id=e.id
        ))
    e.attendees = attendees

    return e


def _users(num: int) -> List[User]:
    users = []

    # Default test account so that we can always login!
    test_user = User(name='Test, Account', email=TEST_ACCOUNT_EMAIL)
    test_user.set_password(TEST_ACCOUNT_PASSWORD)
    users.append(test_user)

    existing_names = set()
    for i in range(0, num - 1):
        gender = random.choice(['M', 'F'])
        name = names.name(gender)

        while name in existing_names:
            name = names.name(gender)

        email = names.email(name)

        u = User(name=name, email=email)
        u.set_password(pwd_generator.password())
        users.append(u)

        existing_names.add(u.name)

    return users


def _patients(num: int, hospitals, users) -> List[Patient]:
    patients = []
    for i in range(0, num):
        gender = random.choice(['M', 'F'])
        name = names.name(gender)
        email = names.email(name)

        patients.append(Patient(
            name=name,
            gender=gender,
            birth_year=date.today().year - random.randint(18, 90),
            email=email,
            address=names.address(),
            phone=names.phone(),
            hospital=random.choice(hospitals),
            created_by=random.choice(users),
            updated_by=random.choice(users)
        ))

    return patients


def _hospitals() -> List[Hospital]:
    hospitals = []
    for city in names.cities:
        name = names.hospital(city)
        address = name + '\n' + city
        hospitals.append(Hospital(name=name, address=address))

    return hospitals


def _surgery(procedure):
    cepod = random.choice(list(Cepod))
    los = random.randint(2, 10)
    date_of_surgery = _date_of_surgery(los)
    date_of_discharge = _date_of_dc(date_of_surgery, los)
    side = random.choice(list(Side))
    primary = random.choice([True, False])
    surgery_type = random.choice(list(Type))
    opd_rv_date = date_of_surgery + timedelta(days=31)
    opd_pain = random.choice(['Yes', 'No'])
    opd_numbness = random.choice(['Yes', 'No'])
    opd_infection = random.choice(['Yes', 'No'])
    opd_comments = random.choice(['All well', 'Terrible'])
    comments = 'sample data set'

    return Surgery(
        cepod=cepod,
        date_of_discharge=date_of_discharge,
        side=side,
        primary=primary,
        type=surgery_type,
        opd_rv_date=opd_rv_date,
        opd_pain=opd_pain,
        opd_numbness=opd_numbness,
        opd_infection=opd_infection,
        opd_comments=opd_comments,
        comments=comments,
        procedure=procedure
    )


def _date_of_surgery(los: int) -> date:
    return date.today() - timedelta(days=random.randint(los, 5 * 365))


def _date_of_dc(date_of_surgery: date, los: int):
    return date_of_surgery + timedelta(days=los)
