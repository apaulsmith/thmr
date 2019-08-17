from flask import render_template, jsonify, request

from app import app, restful
from registry.dao import Dao


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/thmr/data/<string:entity_name>', methods=['GET'])
def get_entity(entity_name):
    dao = Dao.find_dao(app.database.create_session(), entity_name)
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
