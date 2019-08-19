import flask

import config as thmr_config
from app import app
from app.restful import CustomJSONEncoder
from app.session_wrapper import SessionGuard
from registry.schema import Database
from registry.tests import data_generator

if __name__ == '__main__':
    config = thmr_config.Config()
    database = Database(config.DB_URL)

    database.drop_all()
    database.create_all()

    with app.app_context():
        flask.current_app.database = database
        flask.current_app.json_encoder = CustomJSONEncoder
        # flask.current_app.json_decoder = CustomJSONDecoder

    with SessionGuard() as guard:
        data_generator.create_sample_data(guard.session,
                                          num_users=thmr_config.Config.TEST_NUM_USERS,
                                          num_patients=thmr_config.Config.TEST_NUM_PATIENTS)

    app.run(debug=True)
