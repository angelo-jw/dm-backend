from flask import jsonify, request
from app import db
from app.api import bp
from app.models import User
from app.utils.errors import bad_request


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    error = _check_user_data(data)
    if error:
        return error
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    return response


def _check_user_data(data):
    if 'first_name' not in data or 'last_name' not in data or 'email' not in data or 'state' not in data:
        return bad_request('Must include first and last name, email and state fields')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    return None
