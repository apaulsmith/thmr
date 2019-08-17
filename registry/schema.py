import enum
from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

SHORT_TEXT_LENGTH = 60
LONG_TEXT_LENGTH = 240


class Database:
    base = declarative_base()

    def __init__(self, db_url):
        self.engine = sqlalchemy.create_engine(db_url, echo=True)
        self.session = sessionmaker(bind=self.engine, autocommit=False)

    def create_all(self):
        return Database.base.metadata.create_all(self.engine)

    def drop_all(self):
        return Database.base.metadata.drop_all(self.engine)

    def create_session(self):
        return self.session()


class UserType(Database.base):
    __tablename__ = 'UserTypes'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    type = Column(String(SHORT_TEXT_LENGTH), nullable=False, unique=True)

    def __repr__(self):
        return "{}: [id='{}', type='{}']".format(self.__tablename__, self.id, self.type)


class User(Database.base):
    __tablename__ = 'Users'

    id = Column(Integer(), primary_key=True, autoincrement=True)

    type_id = Column(ForeignKey('UserTypes.id'))
    name = Column(String(SHORT_TEXT_LENGTH), nullable=False)
    email = Column(String(SHORT_TEXT_LENGTH), nullable=False)

    def __repr__(self):
        return "{}: [id='{}', type='{}', name='{}', ...]".format(self.__tablename__, self.id, self.type, self.name)


class Patient(Database.base):
    __tablename__ = 'Patients'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(SHORT_TEXT_LENGTH), nullable=False)
    gender = Column(String(1), nullable=False)
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
        return "{}: [id='{}', name='{}', ...]".format(self.__tablename__, self.id, self.name)


class Hospitals(Database.base):
    __tablename__ = 'Hospitals'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(SHORT_TEXT_LENGTH), nullable=False, unique=True)
    address = Column(String(LONG_TEXT_LENGTH), nullable=True)

    def __repr__(self):
        return "{}: [id='{}', name='{}', ...]".format(self.__tablename__, self.id, self.name)


class UsersHospitals(Database.base):
    __tablename__ = 'UsersHospitals'

    user_id = Column(ForeignKey('Users.id'), primary_key=True)
    hospital_id = Column(ForeignKey('Hospitals.id'), primary_key=True)

    def __repr__(self):
        return "{}: [user_id='{}', hospital_id='{}', ...]".format(self.__tablename__, self.user_id, self.hospital_id)


class Operations(Database.base):
    __tablename__ = 'Operations'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    short_name = Column('short_name', String(SHORT_TEXT_LENGTH), nullable=False, unique=True)
    long_name = Column('long_name', String(LONG_TEXT_LENGTH), nullable=True)
    relationship('Surgery', backref=__tablename__)

    def __repr__(self):
        return "{}: [id='{}', short_name='{}', ...]".format(self.__tablename__, self.id, self.short_name)


class Cepod(enum.Enum):
    Immediate = 1
    Urgent = 2
    Expedited = 3
    Elective = 4


class Side(enum.Enum):
    Left = 1
    Right = 2
    NA = 3


class Type(enum.Enum):
    Direct = 1
    Indirect = 2
    NA = 3


class Surgery(Database.base):
    __tablename__ = 'Surgery'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    cepod = Column(Enum(Cepod), nullable=False)
    date_of_surgery = Column(Date, nullable=False)
    date_of_dc = Column(Date, nullable=False)

    operation_id = Column(Integer, ForeignKey('Operations.id'), nullable=False)
    operation = relationship(Operations)

    hospital_id = Column(ForeignKey('Hospitals.id'), nullable=False)
    hospital = relationship(Hospitals)

    side = Column(Enum(Side), nullable=False)
    primary = Column(Boolean, nullable=False, default=True)
    type = Column(Enum(Type), nullable=False)
    additional_procedure = Column(String(LONG_TEXT_LENGTH), nullable=False, default='none')
    antibiotics = Column(String(LONG_TEXT_LENGTH), nullable=False, default='none')
    opd_rv_date = Column(Date, nullable=True)
    opd_pain = Column(String(SHORT_TEXT_LENGTH), nullable=False, default='none')
    opd_numbness = Column(String(SHORT_TEXT_LENGTH), nullable=False, default='none')
    opd_infection = Column(String(SHORT_TEXT_LENGTH), nullable=False, default='none')
    opd_comments = Column(String(LONG_TEXT_LENGTH), nullable=False, default='none')
    comments = Column(String(LONG_TEXT_LENGTH), nullable=False, default='none')

    def __repr__(self):
        return "{}: [id='{}', ...]".format(self.__tablename__, self.id)


class MeshHerniaSurgery(Database.base):
    __tablename__ = 'MeshHerniaSurgery'

    id = Column(ForeignKey('Surgery.id'), nullable=False, primary_key=True)
    type = Column(String(SHORT_TEXT_LENGTH), nullable=False)

    def __repr__(self):
        return "{}: [id='{}', type='{}']".format(self.__tablename__, self.id, self.type)


class SurgeryUsers(Database.base):
    __tablename__ = 'SurgeryUsers'

    user_id = Column(ForeignKey('Users.id'), primary_key=True)
    hospital_id = Column(ForeignKey('Surgery.id'), primary_key=True)

    def __repr__(self):
        return "{}: [user_id='{}', hospital_id='{}']".format(self.__tablename__, self.user_id, self.hospital_id)
