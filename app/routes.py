import logging

from flask import current_app as application
from flask import jsonify, request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import and_
from werkzeug.urls import url_parse

from app import db, login
from app.forms import LoginForm, PatientSearchForm, PatientEditForm, EpisodeEditForm, EpisodeSearchForm
from app.models import User, Patient, Episode, Hospital
from app.dao.dao import Dao
from app.tests import data_generator
from app.util.filter import like_all


@login.user_loader
def load_user(user_id):
    if not isinstance(user_id, int):
        user_id = int(user_id)

    u = db.session.query(User).filter(User.id == user_id).first()
    return u


@application.route('/', methods=['GET'])
def root():
    return redirect(url_for('index'))


@application.route('/not_implemented', methods=['GET'])
def not_implemented():
    return render_template('not_implemented.html', title='Ooops')


@application.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title='Index')


@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if application.config.get('DEFAULT_TEST_ACCOUNT_LOGIN'):
        form.username.data = data_generator.TEST_ACCOUNT_EMAIL
        form.password.data = data_generator.TEST_ACCOUNT_PASSWORD

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        login_msg = 'Login successful for {}'.format(form.username.data)
        logging.info(login_msg)
        flash(login_msg)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@application.route('/patient_search', methods=['GET', 'POST'])
@login_required
def patient_search():
    form = PatientSearchForm()
    form.hospital_id.choices = _hospital_id_choices(include_empty=True)

    if form.validate_on_submit():
        f = like_all({
            Patient.name: form.name.data,
            Patient.email: form.email.data,
            Patient.gender: form.gender.data,
            Patient.phone: form.phone.data,
            Patient.address: form.address.data,
        })

        if form.hospital_id.data != '':
            f.append(Patient.hospital_id == form.hospital_id.data)

        patients = db.session.query(Patient).filter(f).order_by(Patient.name).all()
        return render_template('patient_search.html', title='Patient Search', form=form, results=patients)

    return render_template('patient_search.html', title='Patient Search', form=form)


@application.route('/patient/create', methods=['GET', 'POST'])
@login_required
def patient_create():
    patient = Patient()
    episodes = []

    form = PatientEditForm(obj=patient)
    form.hospital_id.choices = _hospital_id_choices()

    if form.validate_on_submit():
        patient.name = form.name.data
        patient.email = form.email.data
        patient.hospital_id = form.hospital_id.data
        patient.gender = form.gender.data
        patient.phone1 = form.phone.data
        patient.address = form.address.data

        patient.created_by = current_user
        patient.updated_by = current_user

        db.session.add(patient)
        db.session.commit()
        flash('New patient details for {} have been registered.'.format(patient.name))
        return redirect(url_for('patient', id=patient.id))

    return render_template('patient.html', title='Register New Patient', form=form, episodes=episodes)


@application.route('/patient/<int:id>', methods=['GET', 'POST'])
@login_required
def patient(id):
    patient = db.session.query(Patient).filter(Patient.id == id).first()
    episodes = db.session.query(Episode).filter(Episode.patient_id == patient.id).all()

    form = PatientEditForm(obj=patient)
    form.hospital_id.choices = _hospital_id_choices()

    if form.validate_on_submit():
        patient.name = form.name.data
        patient.email = form.email.data
        patient.hospital_id = form.hospital_id.data
        patient.gender = form.gender.data
        patient.phone1 = form.phone.data
        patient.address = form.address.data
        patient.updated_by = current_user

        db.session.commit()

        flash('Patient details have been updated.')
        return redirect(url_for('patient', id=patient.id))

    return render_template('patient.html', title='Patient Details', form=form, episodes=episodes)


@application.route('/episode/<int:id>', methods=['GET', 'POST'])
@login_required
def episode(id):
    episode = db.session.query(Episode).filter(Episode.id == id).first()

    form = EpisodeEditForm(obj=episode)
    form.hospital_id.choices = _hospital_id_choices()
    form.patient_id.choices = _patient_id_choices()

    if form.validate_on_submit():
        episode.episode_type = form.episode_type.data
        episode.date = form.date.data
        episode.patient_id = form.patient_id.data
        episode.hospital_id = form.hospital_id.data
        episode.surgery_id = form.surgery_id.data
        episode.comments = form.comments.data
        episode.updated_by = current_user

        db.session.commit()

        flash('Episode details have been updated.')
        return redirect(url_for('episode', id=episode.id))

    return render_template('episode.html', title='Episode Details', form=form, episode=episode)


@application.route('/episode_search', methods=['GET', 'POST'])
@login_required
def episode_search():
    form = EpisodeSearchForm()
    form.hospital_id.choices = _hospital_id_choices(include_empty=True)
    form.patient_id.choices = _patient_id_choices(include_empty=True)

    if form.is_submitted():
        filter = []
        if form.date.data:
            filter.append(Episode.date == form.date.data)
        if form.episode_type.data:
            filter.append(Episode.episode_type == form.episode_type.data)
        if form.hospital_id.data:
            filter.append(Episode.hospital_id == form.hospital_id.data)
        if form.patient_id.data:
            filter.append(Episode.patient_id == form.patient_id.data)

        episodes = db.session.query(Episode).filter(and_(*filter)).order_by(Episode.date).all()
        return render_template('episode_search.html', title='Episode Search', form=form, results=episodes)

    return render_template('episode_search.html', title='Episode Search', form=form)


@application.route('/episode_create', methods=['GET', 'POST'])
@login_required
def episode_create():
    episode = Episode()
    form = EpisodeEditForm(obj=episode)
    form.hospital_id.choices = _hospital_id_choices()
    form.patient_id.choices = _patient_id_choices()

    if form.validate_on_submit():
        episode.episode_type = form.episode_type.data
        episode.date = form.date.data
        episode.patient_id = form.patient_id.data
        episode.hospital_id = form.hospital_id.data
        episode.surgery_id = form.surgery_id.data
        episode.comments = form.comments.data

        episode.created_by = current_user
        episode.updated_by = current_user

        db.session.add(episode)
        db.session.commit()

        flash('Episode details have been recorded.')
        return redirect(url_for('episode', id=episode.id))

    return render_template('episode.html', title='Record Episode Details', form=form, episode=episode)


@application.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    return redirect(url_for('not_implemented'))


@application.route('/logout')
def logout():
    logout_user()
    flash('Logout successful.')
    return redirect(url_for('index'))


@application.route('/health_check', methods=['GET'])
def health_check():
    if not application:
        raise ValueError('No application running!')

    if db.session.query(User).count() < 1:
        raise ValueError('No users defined!')

    # Return 204 No Content
    return '', 204


@application.route('/thmr/data/<string:entity_name>', methods=['GET'])
def get_entity(entity_name):
    dao = Dao.find_dao(application.database.create_session(), entity_name)

    if request.args.get('flat') is not None:
        return jsonify(restful.all_as_list(dao.find_all()))
    else:
        return jsonify(restful.all_as_dict(dao.find_all()))


@application.route('/thmr/data/<string:entity_name>/<int:id>', methods=['GET'])
def get_entity_by_id(entity_name, id):
    dao = Dao(application.database.create_session(), entity_name)
    return jsonify(restful.one_as_dict(dao.find_id(id)))


@application.route('/thmr/data/<string:entity_name>', methods=['POST'])
def add_entity(entity_name):
    dao = Dao.find_dao(application.database.create_session(), entity_name)
    entity = dao.new(entity_name)

    d = restful.json_loads(request.json)
    entity.from_dict(d)

    return dao.add(entity)


@application.route('/thmr/data/<string:entity_name>/<int:id>', methods=['PUT'])
def update_entity(entity_name, id):
    dao = Dao.find_dao(application.database.create_session(), entity_name)
    d = restful.json_loads(request.json)

    if 'id' in d.keys() and d['id'] != id:
        raise ValueError('The  URL was for id {} but the object sent had id {}!'.format(id, d['id']))
    else:
        d['id'] = id

    return dao.apply_update(d)


def _field_errors(form):
    errors = []
    for field in form:
        for error in field.errors:
            errors.append((field.name, error))

    return errors


def _patient_id_choices(include_empty=False):
    choices = [(str(h.id), h.name) for h in
               db.session.query(Patient).order_by(Patient.name).all()]

    if include_empty:
        choices = [('', '(Any)')] + choices

    return choices


def _hospital_id_choices(include_empty=False):
    choices = [(str(h.id), h.name) for h in
               db.session.query(Hospital).order_by(Hospital.name).all()]

    if include_empty:
        choices = [('', '(Any)')] + choices

    return choices
