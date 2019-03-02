from datetime import datetime, date

from sqlalchemy import MetaData, Table, String, Column, DateTime, Date, Integer, Boolean, ForeignKey

SHORT_TEXT_LENGTH = 60
LONG_TEXT_LENGTH = 240


def build_schema_metadata() -> MetaData:
    metadata = MetaData()

    user_types = Table('UserTypes', metadata,
                       Column('id', Integer(), primary_key=True, autoincrement=True),
                       Column('type', String(SHORT_TEXT_LENGTH), nullable=False, unique=True))

    users = Table('Users', metadata,
                  Column('id', Integer(), primary_key=True, autoincrement=True),
                  Column('type', ForeignKey(user_types.c.id)),
                  Column('name', String(SHORT_TEXT_LENGTH), nullable=False, unique=True),
                  Column('email', String(SHORT_TEXT_LENGTH), nullable=False, unique=True))

    patients = Table('Patients', metadata,
                     Column('id', Integer(), primary_key=True, autoincrement=True),
                     Column('name', String(SHORT_TEXT_LENGTH), nullable=False, unique=True),
                     Column('sex', String(1), nullable=False),
                     Column('age', Integer(), nullable=True),
                     Column('phone1', String(20), nullable=True),
                     Column('phone1', String(20), nullable=True),
                     Column('email', String(SHORT_TEXT_LENGTH), nullable=True),
                     Column('address', String(LONG_TEXT_LENGTH), nullable=True),
                     Column('created_at', DateTime(), default=datetime.now, nullable=False),
                     Column('created_by', ForeignKey(users.c.id), nullable=False),
                     Column('updated_at', DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False),
                     Column('updated_by', ForeignKey(users.c.id), nullable=False))

    hospitals = Table('Hospitals', metadata,
                      Column('id', Integer(), primary_key=True, autoincrement=True),
                      Column('name', String(SHORT_TEXT_LENGTH), nullable=False, unique=True),
                      Column('address', String(LONG_TEXT_LENGTH), nullable=True))

    users_hospitals = Table('UsersHospitals', metadata,
                            Column('user_id', ForeignKey(users.c.id)),
                            Column('hospital_id', ForeignKey(hospitals.c.id)))

    operations = Table('Operations', metadata,
                       Column('id', Integer(), primary_key=True, autoincrement=True),
                       Column('short_name', String(SHORT_TEXT_LENGTH), nullable=False, unique=True),
                       Column('long_name', String(LONG_TEXT_LENGTH), nullable=True))

    surgery = Table('Surgery', metadata,
                    Column('id', Integer(), primary_key=True, autoincrement=True),
                    Column('cepod', String(SHORT_TEXT_LENGTH), nullable=False),
                    Column('date_of_surgery', Date, nullable=False),
                    Column('date_of_dc', Date, nullable=False),
                    Column('los', Integer, nullable=False),
                    Column('operation', ForeignKey(operations.c.id), nullable=False),
                    Column('side', String(5), nullable=False),
                    Column('primary', Boolean, nullable=False, default=True),
                    Column('type', String(SHORT_TEXT_LENGTH), nullable=False),
                    Column('additional_procedure', String(LONG_TEXT_LENGTH), nullable=False, default='none'),
                    Column('antibiotics', String(LONG_TEXT_LENGTH), nullable=False, default='none'),
                    Column('interval', Integer, nullable=False, default=0),
                    Column('opd_rv_date', Date, nullable=False, default=date.today),
                    Column('opd_pain', String(SHORT_TEXT_LENGTH), nullable=False, default='none'),
                    Column('opd_numbness', String(SHORT_TEXT_LENGTH), nullable=False, default='none'),
                    Column('opd_infection', String(SHORT_TEXT_LENGTH), nullable=False, default='none'),
                    Column('opd_comments', String(LONG_TEXT_LENGTH), nullable=False, default='none'),
                    Column('comments', String(LONG_TEXT_LENGTH), nullable=False, default='none'))

    users_surgery = Table('SurgeryUsers', metadata,
                            Column('user_id', ForeignKey(users.c.id)),
                            Column('hospital_id', ForeignKey(surgery.c.id)))

    return metadata

def db_engine():
    pass