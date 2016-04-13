from flask import redirect, render_template, request, session, url_for, g

from app import app
from app.decorators import has_rights, login_required
from app.models import User


@app.route('/')
@login_required
def index():
    return render_template('list.html', users=User.query.all())


@app.route('/user', methods=['POST', 'GET'])
@app.route('/user/<int:user_id>', methods=['POST', 'GET'])
@login_required
@has_rights
def user_edit(user_id=None):
    if user_id and g.current_user.id != user_id:
        user = User.get(user_id)
    else:
        user = None

    if request.method == "POST":
        if user:
            user.username = request.form['username']
            user.full_rights = True if request.form.get('full_rights') else False
            user.save()
        else:
            user = User(request.form['username'], request.form['password'],
                        full_rights=True if request.form.get('full_rights') else False)
            user.create()

        return redirect(url_for('index'))

    return render_template('edit.html', user=user)


@app.route('/user/<int:user_id>/remove', methods=['POST'])
@login_required
@has_rights
def user_remove(user_id):
    user = User.get(user_id)

    if user and user.id != g.current_user.id:
        user.remove()

    return redirect(url_for('index'))


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
