from functools import wraps
from flask import g, request, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            _ = g.current_user
        except AttributeError:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def has_rights(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            current_user = g.current_user
        except AttributeError:
            current_user = None

        if current_user and current_user.full_rights:
            return f(*args, **kwargs)

        return "Forbidden", 403
    return decorated_function
