from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, \
    HiddenField
from wtforms.ext.dateutil.fields import DateField
from wtforms.validators import DataRequired

from app.models import EpisodeType


def choice_for_enum(enum, include_blank=False):
    l = [(e, e.name) for e in enum]
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
            id = int(name)
            try:
                return enum(id)
            except KeyError:
                raise ValueError(name)
        except ValueError:
            try:
                if '.' in name:
                    name = name[name.find('.')+1:]
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
    hospital_id = SelectField('Hospital')
    gender = SelectField('Gender', choices=[('', 'Any'), ('M', 'Male'), ('F', 'Female')])
    phone = StringField('Phone #')
    address = TextAreaField('Address')
    created_by = HiddenField('Created By')
    created_at = HiddenField('Created At')
    updated_by = HiddenField('Updated By')
    updated_at = HiddenField('Updated At')


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
    created_by = HiddenField('Created By')
    created_at = HiddenField('Created At')
    updated_by = HiddenField('Updated By')
    updated_at = HiddenField('Updated At')


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
