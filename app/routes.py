from flask import render_template, jsonify

from app import app, restful
from registry.dao import Dao
from registry.schema import Hospital


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/thmr/data/<string:entity>', methods=['GET'])
def get_entity(entity):
    dao = Dao.find_dao(app.database.create_session(), entity)
    return jsonify(restful.all_as_dict(dao.find_all()))


@app.route('/thmr/data/<string:entity>/<int:id>', methods=['GET'])
def get_entity_by_id(entity, id):
    dao = Dao(app.database.create_session(), Hospital)
    return jsonify(restful.all_as_dict(dao.find_all()))
