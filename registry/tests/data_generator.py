import random
from typing import List

from registry.schema import UserTypes, Users, Patients
from registry.tests import names


def create_sample_data(session, num_users: int, num_patients: int):
    session.add(_user_types(session))
    session.add(_users(num_users))
    session.add(_patients(num_patients))


def _user_types(session):
    user_types = []
    if not session.query(UserTypes).filter_by(type='Surgeon').exists():
        user_types.append(UserTypes(type='Surgeon'))

    if not session.query(UserTypes).filter_by(type='Nurse').exists():
        user_types.append(UserTypes(type='Nurse'))

    if not session.query(UserTypes).filter_by(type='Patient').exists():
        user_types.append(UserTypes(type='Patient'))

    return user_types


def _users(num: int) -> List[Users]:
    users = []
    for i in range(0, num):
        gender = random.choice(['M', 'F'])
        name = names.name(gender)
        email = names.email(name)
        user_type = random.choice(_user_types())

        users.append(Users(type=user_type, name=name, email=email))

    return users


def _patients(num: int) -> List[Patients]:
    patients = []
    for i in range(0, num):
        gender = random.choice(['M', 'F'])
        name = names.name(gender)
        age = random.randint(18, 90)
        email = names.email(name)
        address = names.address()

        patients.append(Patients(
            name=name,
            gender=gender,
            age=age,
            email=email,
            address=address
        ))

    return patients
