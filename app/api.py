from flask import g, request, jsonify

from app import app
from app.decorators import has_rights, login_required
from app.models import User
from app.views import logout


@app.route('/api/user', methods=['POST'])
@app.route('/api/user/<int:user_id>', methods=['PUT', 'DELETE'])
@login_required
@has_rights
def user(user_id=None):
    status = True
    code = 202
    full_rights = (request.form.get('full_rights') == 'true')

    if request.method == "POST":
        user = User(request.form['username'], request.form['password'], full_rights=full_rights)
        user.save()
        code = 201
    else:
        user = User.get(user_id)

        if request.method == 'DELETE':
            user.remove()
        else:
            user.username = request.form['username']
            password = request.form['password']
            if password:
                user.set_password(password)
            user.full_rights = full_rights
            user.save()

        if user.id == g.current_user.id and (request.method == 'DELETE' or not full_rights):
            logout()
            return jsonify({'status': status, 'reload': True})

    return jsonify({'status': status, 'user': {'id': user.id, 'username': user.username,
                                               'full_rights': user.full_rights}}), code
