from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, \
    HiddenField
from wtforms.ext.dateutil.fields import DateField
from wtforms.validators import DataRequired

from registry.schema import EpisodeType


def choice_for_enum(enum, include_blank=False):
    l = [(e.value, e.name) for e in enum]
    if include_blank:
        l.insert(0, ('', '(Any)'))
    return l


def coerce_for_enum(enum):
    def coerce(name):
        if name is None or str(name) == '':
            return None

        if isinstance(name, enum):
            return name
        try:
            try:
                id = int(name)
                return enum(id)
            except ValueError:
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


class EpisodeForm(FlaskForm):
    date = DateField('Date')
    patient_id = SelectField('Patient')
    hospital_id = SelectField('Hospital')
    surgery_id = HiddenField('Surgery')
    comments = TextAreaField('Comments')


class EpisodeEditForm(EpisodeForm):
    episode_type = SelectField('Episode Type',
                               choices=choice_for_enum(EpisodeType, include_blank=False),
                               coerce=coerce_for_enum(EpisodeType))
    submit = SubmitField('Save Changes')


class EpisodeSearchForm(EpisodeForm):
    episode_type = SelectField('Episode Type',
                               choices=choice_for_enum(EpisodeType, include_blank=True),
                               coerce=coerce_for_enum(EpisodeType))
    submit = SubmitField('Search')
