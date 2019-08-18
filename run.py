import argparse

import flask

import config as thmr_config
from app import app
from app.restful import CustomJSONEncoder, CustomJSONDecoder
from config import Config
from registry.schema import Database
from registry.tests import data_generator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tanzanian Hernia Mesh Registry')
    parser.add_argument('--drop-all', default=False, action='store_true')
    parser.add_argument('--create-all', default=False, action='store_true')
    parser.add_argument('--generate', help='Generate and write dummy test data into the database',
                        default=False, action='store_true')
    parser.add_argument('--flask', help='Run the flask application', default=False, action='store_true')

    args = parser.parse_args()

    config = thmr_config.Config()
    database = Database(config.DB_URL)

    if args.drop_all:
        database.drop_all()

    if args.create_all:
        database.create_all()

    if args.generate:
        session = database.create_session()
        with session.begin_nested():
            data_generator.create_sample_data(session,
                                              num_users=thmr_config.Config.TEST_NUM_USERS,
                                              num_patients=thmr_config.Config.TEST_NUM_PATIENTS,
                                              num_surgeries=thmr_config.Config.TEST_NUM_SURGERIES)
        session.close()

    if args.flask:
        with app.app_context():
            flask.current_app.database = database
            flask.current_app.json_encoder = CustomJSONEncoder
            # flask.current_app.json_decoder = CustomJSONDecoder

        app.run(debug=True)
