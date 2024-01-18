from flask import jsonify, request
from firebase_admin import auth
from functools import wraps

from app.api import bp
from app.utils.errors import bad_request
from app.controllers import user as user_controller


@bp.route('auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}
        _check_user_data(data)
        user_token = user_controller.login(data=data)
        response = jsonify({
            "message": "User logged in successfully",
            "token": user_token
        })
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


def _check_user_data(data):
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data:
            raise Exception(f"Missing required field {field}")
    return None


def validate(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.headers.get('Authorization'):
            return bad_request('Missing token')
        try:
            user = auth.verify_id_token(request.headers['Authorization'])
            request.user = user
        except Exception:
            return bad_request('Invalid token')
        return f(*args, **kwargs)
    return wrap
