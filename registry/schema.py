import enum
from datetime import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from werkzeug.security import generate_password_hash, check_password_hash

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


class ExtendedBase:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def from_dict(self, d):
        for k, v in d.items():
            setattr(self, k, v)


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


#
# This is necessary so that the Custom JSONEncoder/Decoder in restful.py can know which enums to
# encode or decode.
#
KNOWN_ENUMS = {
    'Cepod': Cepod,
    'Side': Side,
    'Type': Type
}


class UserType(Database.base, ExtendedBase):
    __tablename__ = 'UserTypes'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    type = Column(String(SHORT_TEXT_LENGTH), nullable=False, unique=True)

    def __repr__(self):
        return "{}: [id='{}', type='{}']".format(self.__tablename__, self.id, self.type)


class User(Database.base, ExtendedBase, UserMixin):
    __tablename__ = 'Users'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
    type_id = Column(ForeignKey('UserTypes.id'))
    name = Column(String(SHORT_TEXT_LENGTH), nullable=False)
    email = Column(String(SHORT_TEXT_LENGTH), nullable=False)
    password_hash = Column(String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return "{}: [id='{}', name='{}', email='{}'...]".format(self.__tablename__, self.id, self.name, self.email)


class Patient(Database.base, ExtendedBase):
    __tablename__ = 'Patients'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
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

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return "{}: [id='{}', name='{}', ...]".format(self.__tablename__, self.id, self.name)


class Hospital(Database.base, ExtendedBase):
    __tablename__ = 'Hospitals'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
    name = Column(String(SHORT_TEXT_LENGTH), nullable=False, unique=True)
    address = Column(String(LONG_TEXT_LENGTH), nullable=True)

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return "{}: [id='{}', name='{}', ...]".format(self.__tablename__, self.id, self.name)


class UsersHospital(Database.base, ExtendedBase):
    __tablename__ = 'UsersHospitals'

    user_id = Column(ForeignKey('Users.id'), primary_key=True)
    hospital_id = Column(ForeignKey('Hospitals.id'), primary_key=True)

    def __repr__(self):
        return "{}: [user_id='{}', hospital_id='{}', ...]".format(self.__tablename__, self.user_id, self.hospital_id)


class Operation(Database.base, ExtendedBase):
    __tablename__ = 'Operations'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
    name = Column('name', String(SHORT_TEXT_LENGTH), nullable=False, unique=True)
    long_name = Column('long_name', String(LONG_TEXT_LENGTH), nullable=True)
    relationship('Surgery', backref=__tablename__)

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return "{}: [id='{}', name='{}', ...]".format(self.__tablename__, self.id, self.name)


class Surgery(Database.base, ExtendedBase):
    __tablename__ = 'Surgery'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)

    cepod = Column(Enum(Cepod), nullable=False)
    date_of_surgery = Column(Date, nullable=False)
    date_of_dc = Column(Date, nullable=False)

    operation_id = Column(Integer, ForeignKey('Operations.id'), nullable=False)
    operation = relationship(Operation)

    hospital_id = Column(ForeignKey('Hospitals.id'), nullable=False)
    hospital = relationship(Hospital)

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

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return "{}: [id='{}', ...]".format(self.__tablename__, self.id)


class MeshHerniaSurgery(Database.base, ExtendedBase):
    __tablename__ = 'MeshHerniaSurgery'

    id = Column(ForeignKey('Surgery.id'), nullable=False, primary_key=True)
    version_id = Column(Integer, nullable=False)
    type = Column(String(SHORT_TEXT_LENGTH), nullable=False)

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return "{}: [id='{}', type='{}']".format(self.__tablename__, self.id, self.type)


class SurgeryUser(Database.base, ExtendedBase):
    __tablename__ = 'SurgeryUsers'

    user_id = Column(ForeignKey('Users.id'), primary_key=True)
    hospital_id = Column(ForeignKey('Surgery.id'), primary_key=True)

    def __repr__(self):
        return "{}: [user_id='{}', hospital_id='{}']".format(self.__tablename__, self.user_id, self.hospital_id)
