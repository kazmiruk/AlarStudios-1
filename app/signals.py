from flask import g, session

from app import app
from app.models import User


@app.before_request
def before_request():
    user_id = session.get('user_id')

    if user_id is not None:
        setattr(g, 'current_user', User.get(user_id))
