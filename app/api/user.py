from flask import jsonify, request

from app.api import bp
from app.utils.errors import bad_request
from app.controllers import user as user_controller


@bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json() or {}
        _check_user_data(data)
        user = user_controller.create_user(data=data)
        response = jsonify({
            "message": "User created successfully",
            "user": user
        })
        response.status_code = 201
        return response
    except Exception as e:
        return bad_request(str(e))


def _check_user_data(data):
    required_fields = ['first_name', 'last_name', 'email', 'state', 'password']
    for field in required_fields:
        if field not in data:
            raise Exception(f"Missing required field {field}")
    return None
