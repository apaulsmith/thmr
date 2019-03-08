from datetime import datetime, date

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

import config

SHORT_TEXT_LENGTH = 60
LONG_TEXT_LENGTH = 240


class Database:
    engine = sqlalchemy.create_engine(config.DB_URL, echo=True)
    base = declarative_base()

    @staticmethod
    def create_schema():
        return Database.base.metadata.create_all(Database.engine)


class UserTypes(Database.base):
    __tablename__ = 'UserTypes'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    type = Column(String(SHORT_TEXT_LENGTH), nullable=False, unique=True)

    def __repr__(self):
        return "%s: [id='%d', type='%s']".format(self.__tablename__, self.id, self.type)


class Users(Database.base):
    __tablename__ = 'Users'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    type = Column(ForeignKey('UserTypes.id'))
    name = Column(String(SHORT_TEXT_LENGTH), nullable=False, unique=True)
    email = Column(String(SHORT_TEXT_LENGTH), nullable=False, unique=True)

    def __repr__(self):
        return "%s: [id='%d', type='%s', name='%s', ...]".format(self.__tablename__, self.id, self.type, self.name)


class Patients(Database.base):
    __tablename__ = 'Patients'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(SHORT_TEXT_LENGTH), nullable=False, unique=True)
    sex = Column(String(1), nullable=False)
    age = Column(Integer(), nullable=True)
    phone1 = Column(String(20), nullable=True)
    phone2 = Column(String(20), nullable=True)
    email = Column(String(SHORT_TEXT_LENGTH), nullable=True)
    address = Column(String(LONG_TEXT_LENGTH), nullable=True)
    created_at = Column('created_at', DateTime(), default=datetime.now, nullable=False)
    created_by = Column('created_by', ForeignKey('Users.id'), nullable=False)
    updated_at = Column('updated_at', DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    updated_by = Column('updated_by', ForeignKey('Users.id'), nullable=False)

    def __repr__(self):
        return "%s: [id='%d', name='%s', ...]".format(self.__tablename__, self.id, self.name)


class Hospitals(Database.base):
    __tablename__ = 'Hospitals'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(SHORT_TEXT_LENGTH), nullable=False, unique=True)
    address = Column(String(LONG_TEXT_LENGTH), nullable=True)

    def __repr__(self):
        return "%s: [id='%d', name='%s', ...]".format(self.__tablename__, self.id, self.name)


class UsersHospitals(Database.base):
    __tablename__ = 'UsersHospitals'

    user_id = Column(ForeignKey('Users.id'), primary_key=True)
    hospital_id = Column(ForeignKey('Hospitals.id'), primary_key=True)

    def __repr__(self):
        return "%s: [user_id='%d', hospital_id='%d', ...]".format(self.__tablename__, self.user_id, self.hospital_id)


class Operations(Database.base):
    __tablename__ = 'Operations'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    short_name = Column('short_name', String(SHORT_TEXT_LENGTH), nullable=False, unique=True)
    long_name = Column('long_name', String(LONG_TEXT_LENGTH), nullable=True)

    def __repr__(self):
        return "%s: [id='%d', short_name='%s', ...]".format(self.__tablename__, self.id, self.short_name)


class Surgery(Database.base):
    __tablename__ = 'Surgery'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    cepod = Column(String(SHORT_TEXT_LENGTH), nullable=False)
    date_of_surgery = Column(Date, nullable=False)
    date_of_dc = Column(Date, nullable=False)
    los = Column(Integer, nullable=False)
    operation = Column(ForeignKey('Operations.id'), nullable=False)
    side = Column(String(5), nullable=False)
    primary = Column(Boolean, nullable=False, default=True)
    type = Column(String(SHORT_TEXT_LENGTH), nullable=False)
    additional_procedure = Column(String(LONG_TEXT_LENGTH), nullable=False, default='none')
    antibiotics = Column(String(LONG_TEXT_LENGTH), nullable=False, default='none')
    interval = Column(Integer, nullable=False, default=0)
    opd_rv_date = Column(Date, nullable=False, default=date.today)
    opd_pain = Column(String(SHORT_TEXT_LENGTH), nullable=False, default='none')
    opd_numbness = Column(String(SHORT_TEXT_LENGTH), nullable=False, default='none')
    opd_infection = Column(String(SHORT_TEXT_LENGTH), nullable=False, default='none')
    opd_comments = Column(String(LONG_TEXT_LENGTH), nullable=False, default='none')
    comments = Column(String(LONG_TEXT_LENGTH), nullable=False, default='none')

    def __repr__(self):
        return "%s: [id='%d', ...]".format(self.__tablename__, self.id)


class SurgeryUsers(Database.base):
    __tablename__ = 'SurgeryUsers'

    user_id = Column(ForeignKey('Users.id'), primary_key=True)
    hospital_id = Column(ForeignKey('Surgery.id'), primary_key=True)

    def __repr__(self):
        return "%s: [user_id='%d', hospital_id='%d']".format(self.__tablename__, self.user_id, self.hospital_id)
