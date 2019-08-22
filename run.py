import argparse

from app import create_app
from registry.tests import data_generator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tanzania Mesh Hernia Repository')
    parser.add_argument('--reset-db', help='drop and create the database', action='store_true')
    parser.add_argument('--generate', help='generate dummy test data', action='store_true')
    parser.add_argument('--no-flask', help='generate dummy test data', dest='flask', action='store_false')
    parser.add_argument('--flask', help='generate dummy test data', dest='flask', action='store_true', default=True)
    args = parser.parse_args()

    application = create_app()
    with application.app_context():

        if args.reset_db:
            application.db.create_all()

        if args.generate:
            session = application.db.session
            with session.begin_nested():
                data_generator.create_sample_data(session,
                                                  num_users=12,
                                                  num_patients=50)
            session.commit()

    if args.flask:
        application.run(debug=True)
