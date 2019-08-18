from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired


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
