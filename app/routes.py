from flask import jsonify, request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, restful
from app.forms import LoginForm
from registry.dao import Dao
from registry.schema import User


@app.route('/thmr/ui/registry', methods=['GET'])
def ui_registry():
    return render_template("registry.html")


@app.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title='Index')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session = app.database.create_session()
        user = session.query(User).filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Login successful for {}'.format(form.username.data))

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Logout successful.')
    return redirect(url_for('index'))


@app.route('/thmr/data/<string:entity_name>', methods=['GET'])
def get_entity(entity_name):
    dao = Dao.find_dao(app.database.create_session(), entity_name)

    if request.args.get('flat') is not None:
        return jsonify(restful.all_as_list(dao.find_all()))
    else:
        return jsonify(restful.all_as_dict(dao.find_all()))


@app.route('/thmr/data/<string:entity_name>/<int:id>', methods=['GET'])
def get_entity_by_id(entity_name, id):
    dao = Dao(app.database.create_session(), entity_name)
    return jsonify(restful.one_as_dict(dao.find_id(id)))


@app.route('/thmr/data/<string:entity_name>', methods=['POST'])
def add_entity(entity_name):
    dao = Dao.find_dao(app.database.create_session(), entity_name)
    entity = dao.new(entity_name)

    d = restful.json_loads(request.json)
    entity.from_dict(d)

    return dao.add(entity)


@app.route('/thmr/data/<string:entity_name>/<int:id>', methods=['PUT'])
def update_entity(entity_name, id):
    dao = Dao.find_dao(app.database.create_session(), entity_name)
    d = restful.json_loads(request.json)

    if 'id' in d.keys() and d['id'] != id:
        raise ValueError('The  URL was for id {} but the object sent had id {}!'.format(id, d['id']))
    else:
        d['id'] = id

    return dao.apply_update(d)
