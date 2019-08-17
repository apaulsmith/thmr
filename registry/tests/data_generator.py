import random
from typing import List

from registry.schema import UserType, User, Patient
from registry.tests import names


def create_sample_data(session, num_users: int, num_patients: int):
    session.add_all(_user_types(session))

    user_type_count = session.query(UserType).count()
    for user_type in session.query(UserType).all():
        session.add_all(_users(user_type, int(num_users / user_type_count)))

    session.add_all(_patients(num_patients))


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
