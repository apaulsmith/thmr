from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, DateField, \
    HiddenField
from wtforms.validators import DataRequired

from registry.schema import EpisodeType


def choice_for_enum(enum):
    return [e.name for e in enum]


def coerce_for_enum(enum):
    def coerce(name):
        if isinstance(name, enum):
            return name
        try:
            return enum[name]
        except KeyError:
            raise ValueError(name)

    return coerce


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class PatientForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    gender = SelectField('Gender', choices=[('', 'Any'), ('M', 'Male'), ('F', 'Female')])
    phone = StringField('Phone #')
    address = TextAreaField('Address')


class PatientSearchForm(PatientForm):
    submit = SubmitField('Search')


class PatientEditForm(PatientForm):
    submit = SubmitField('Save Changes')


class EpisodeEditForm(FlaskForm):
    episode_type = HiddenField('Episode Type')
    date = DateField('Date')
    patient_id = HiddenField('Patient')
    hospital_id = HiddenField('Hospital')
    surgery_id = HiddenField('Surgery')
    comments = TextAreaField('Comments')
    submit = SubmitField('Save Changes')
