from app import app, login
from registry.schema import User


@login.user_loader
def load_user(id):
    session = app.database.create_session()
    return session.query(User).filter_by(id=int(id)).first()
