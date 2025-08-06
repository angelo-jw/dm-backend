from flask import jsonify, request

from app.api import bp
from app.utils.errors import bad_request, not_found
from app.controllers import user as user_controller
from app.utils.auth import validate


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
    

@bp.route('/users/me', methods=['GET'])
@validate
def get_me():
    try:
        user_id = request.user.get("uid")
        user = user_controller.get_user_by_id(uid=user_id)
        if not user:
            return not_found("User not found")

        response = jsonify(user)
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route('/users/me', methods=['PUT'])
@validate
def update_me():
    try:
        user_id = request.user.get('uid')
        data = request.get_json() or {}

        user_controller.update_user(uid=user_id, data=data)

        response = jsonify({"message": "User updated successfully"})
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


def _check_user_data(data):
    required_fields = ['first_name', 'last_name', 'email', 'state', 'password']
    for field in required_fields:
        if field not in data:
            raise Exception(f"Missing required field {field}")
    return None
