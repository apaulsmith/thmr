from app import app
from registry.schema import Database

if __name__ == '__main__':
    app.database = Database()
    app.run()
