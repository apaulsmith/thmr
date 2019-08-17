import argparse

import config as thmr_config
from app import app
from registry.schema import Database
from registry.tests import data_generator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tanzanian Hernia Mesh Registry')
    parser.add_argument('--drop-all', default=False, action='store_true')
    parser.add_argument('--create-all', default=False, action='store_true')
    parser.add_argument('--generate', help='Generate and write dummy test data into the database',
                        default=False, action='store_true')
    parser.add_argument('--run-flask', help='Run the flask application', default=False, action='store_true')

    args = parser.parse_args()

    app.database = Database(thmr_config.DB_URL)

    if args.drop_all:
        app.database.drop_all()

    if args.create_all:
        app.database.create_all()

    if args.generate_test_data:
        session = app.database.create_session()
        with session.begin_nested():
            data_generator.create_sample_data(session,
                                              num_users=thmr_config.TEST_NUM_USERS,
                                              num_patients=thmr_config.TEST_NUM_PATIENTS,
                                              num_surgeries=thmr_config.TEST_NUM_SURGERIES)
        session.close()

    if args.run_flask:
        app.run()
