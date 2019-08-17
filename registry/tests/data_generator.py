import random
from datetime import timedelta, date
from typing import List

from registry.schema import UserType, User, Patient, Hospitals, Operations, Surgery, Side, Type, Cepod
from registry.tests import names


def create_sample_data(session, num_users: int, num_patients: int, num_surgeries: int):
    session.add_all(_user_types(session))

    user_type_count = session.query(UserType).count()
    for user_type in session.query(UserType).all():
        session.add_all(_users(user_type, int(num_users / user_type_count)))

    session.add_all(_patients(num_patients))
    session.add_all(_hospitals())
    session.add_all(_operations())

    session.add_all(_surgeries(session, num_surgeries))


def _user_types(session):
    user_types = []
    if session.query(UserType).filter_by(type='Surgeon').count() == 0:
        user_types.append(UserType(type='Surgeon'))

    if session.query(UserType).filter_by(type='Nurse').count() == 0:
        user_types.append(UserType(type='Nurse'))

    if session.query(UserType).filter_by(type='Patient').count() == 0:
        user_types.append(UserType(type='Patient'))

    return user_types


def _users(user_type: UserType, num: int) -> List[User]:
    users = []
    for i in range(0, num):
        gender = random.choice(['M', 'F'])
        name = names.name(gender)
        email = names.email(name)

        users.append(User(type_id=user_type.id, name=name, email=email))

    return users


def _patients(num: int) -> List[Patient]:
    patients = []
    for i in range(0, num):
        gender = random.choice(['M', 'F'])
        name = names.name(gender)
        age = random.randint(18, 90)
        email = names.email(name)
        address = names.address()

        patients.append(Patient(
            name=name,
            gender=gender,
            age=age,
            email=email,
            address=address,
            created_by=1,
            updated_by=1,
        ))

    return patients


def _hospitals() -> List[Hospitals]:
    hospitals = []
    for city in names.cities:
        name = names.hospital(city)
        address = name + '\n' + city
        hospitals.append(Hospitals(name=name, address=address))

    return hospitals


def _operations() -> List[Operations]:
    operations = []
    for operation in names.operations:
        operations.append(Operations(short_name=operation, long_name='long name for {}'.format(operation)))

    return operations


def _surgeries(session, num: int):
    surgeries = []
    for i in range(0, num):
        cepod = random.choice(list(Cepod))
        los = random.randint(2, 10)
        date_of_surgery = _date_of_surgery(los)
        date_of_dc = _date_of_dc(date_of_surgery, los)
        operation = random.choice(session.query(Operations).all())
        hospital = random.choice(session.query(Hospitals).all())
        side = random.choice(list(Side))
        primary = random.choice([True, False])
        surgery_type = random.choice(list(Type))
        opd_rv_date = date_of_surgery + timedelta(days=31)
        opd_pain = random.choice(['Yes', 'No'])
        opd_numbness = random.choice(['Yes', 'No'])
        opd_infection = random.choice(['Yes', 'No'])
        opd_comments = random.choice(['All well', 'Terrible'])
        comments = 'sample data set'

        surgeries.append(Surgery(
            cepod=cepod,
            date_of_surgery=date_of_surgery,
            date_of_dc=date_of_dc,
            operation=operation,
            hospital=hospital,
            side=side,
            primary=primary,
            type=surgery_type,
            opd_rv_date=opd_rv_date,
            opd_pain=opd_pain,
            opd_numbness=opd_numbness,
            opd_infection=opd_infection,
            opd_comments=opd_comments,
            comments=comments
        ))

    return surgeries


def _date_of_surgery(los: int):
    return date.today() - timedelta(days=random.randint(los, 5 * 365))


def _date_of_dc(date_of_surgery: date, los: int):
    return date_of_surgery + timedelta(days=los)
