from flask import g

from app import app


@app.context_processor
def inject_user():
    return dict(current_user=g.current_user if 'current_user' in g else None)
