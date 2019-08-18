from app import app, login
from app.session_wrapper import SessionGuard
from registry.schema import User


@login.user_loader
def load_user(id):
    with SessionGuard() as guard:
        return guard.session.query(User).filter_by(id=int(id)).first()
