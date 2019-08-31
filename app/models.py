import enum
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Enum, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

SHORT_TEXT_LENGTH = 60
LONG_TEXT_LENGTH = 240


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


class EpisodeType(enum.Enum):
    Surgery = 1
    FollowUp = 2
    Other = 3


#
# This is necessary so that the Custom JSONEncoder/Decoder in restful.py can know which enums to
# encode or decode.
#
KNOWN_ENUMS = {
    'Cepod': Cepod,
    'Side': Side,
    'Type': Type,
    'EpisodeType': EpisodeType,
}


class Hospital(db.Model, ExtendedBase):
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


class User(db.Model, ExtendedBase, UserMixin):
    __tablename__ = 'Users'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
    name = Column(String(SHORT_TEXT_LENGTH), unique=True, nullable=False)
    email = Column(String(SHORT_TEXT_LENGTH), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return self.name


class EpisodeAttendee(db.Model, ExtendedBase):
    __tablename__ = 'EpisodeAttendees'

    user_id = Column(ForeignKey('Users.id'), primary_key=True)
    user = relationship(User)

    episode_id = Column(ForeignKey('Episodes.id'), primary_key=True)
    comments = Column(String(LONG_TEXT_LENGTH), nullable=False, default='none')

    def __repr__(self):
        return "{}: [user_id='{}', hospital_id='{}']".format(self.__tablename__, self.user_id, self.hospital_id)


class Patient(db.Model, ExtendedBase):
    __tablename__ = 'Patients'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
    name = Column(String(SHORT_TEXT_LENGTH), nullable=False)
    gender = Column(String(1), nullable=False)
    birth_year = Column(Integer(), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(SHORT_TEXT_LENGTH), nullable=True)
    address = Column(String(LONG_TEXT_LENGTH), nullable=True)

    hospital_id = Column(ForeignKey('Hospitals.id'), nullable=False)
    hospital = relationship(Hospital)

    created_at = Column('created_at', DateTime(), default=datetime.now, nullable=False)
    created_by_id = Column(ForeignKey('Users.id'), nullable=False)
    created_by = relationship(User, foreign_keys=[created_by_id])

    updated_at = Column('updated_at', DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    updated_by_id = Column(ForeignKey('Users.id'), nullable=False)
    updated_by = relationship(User, foreign_keys=[updated_by_id])

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return self.name


class Complication(db.Model, ExtendedBase):
    __tablename__ = 'Complications'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)

    episode_id = Column(ForeignKey('Episodes.id'), nullable=False)

    date = Column(Date, nullable=False, default=datetime.today())
    comments = Column('comments', String(LONG_TEXT_LENGTH))

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return "{}: [id='{}', name='{}', ...]".format(self.__tablename__, self.id, self.name)


class Procedure(db.Model, ExtendedBase):
    __tablename__ = 'Procedures'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
    name = Column('name', String(SHORT_TEXT_LENGTH), nullable=False, unique=True)

    relationship('Surgery', backref=__tablename__)

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return "{}: [id='{}', name='{}', ...]".format(self.__tablename__, self.id, self.name)


class Surgery(db.Model, ExtendedBase):
    __tablename__ = 'Surgeries'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)

    cepod = Column(Enum(Cepod), nullable=False)
    date_of_discharge = Column(Date, nullable=True)

    procedure_id = Column(Integer, ForeignKey('Procedures.id'), nullable=False)
    procedure = relationship(Procedure)

    episode = relationship('Episode', uselist=False)

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


class Episode(db.Model, ExtendedBase):
    __tablename__ = 'Episodes'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    version_id = Column(Integer, nullable=False)
    episode_type = Column(Enum(EpisodeType), nullable=False)
    date = Column(Date, nullable=False, default=datetime.today())

    patient_id = Column(ForeignKey('Patients.id'), nullable=False)
    patient = relationship(Patient)

    hospital_id = Column(ForeignKey('Hospitals.id'), nullable=False)
    hospital = relationship(Hospital)

    attendees = relationship('EpisodeAttendee')

    surgery_id = Column(ForeignKey('Surgeries.id'), nullable=True)
    surgery = relationship(Surgery)

    complications = relationship(Complication)
    comments = Column(String(LONG_TEXT_LENGTH), nullable=False, default='none')

    created_at = Column('created_at', DateTime(), default=datetime.now, nullable=False)
    created_by_id = Column(ForeignKey('Users.id'), nullable=False)
    created_by = relationship(User, foreign_keys=[created_by_id])

    updated_at = Column('updated_at', DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    updated_by_id = Column(ForeignKey('Users.id'), nullable=False)
    updated_by = relationship(User, foreign_keys=[updated_by_id])

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return "{}: [id='{}', date='{}', patient='{}', hospital='{}', ...]".format(self.__tablename__,
                                                                                   self.id,
                                                                                   self.date.isoformat(),
                                                                                   self.patient_id,
                                                                                   self.hospital_id)
