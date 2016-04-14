from flask import redirect, render_template, request, session, url_for, g

from app import app
from app.decorators import login_required
from app.models import User


@app.route('/')
@login_required
def index():
    return render_template('list.html', users=User.query.all())


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        user = User.authenticate(request.form['username'], request.form['password'])

        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))

        error = 'Invalid username/password'

    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
