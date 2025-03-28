from flask import jsonify, request
from firebase_admin import auth
from functools import wraps

from app.api import bp
from app.utils.errors import unauthorized, forbidden
from app.controllers import user as user_controller


@bp.route("auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json() or {}
        _check_user_data(data)
        user_info = user_controller.login(data=data)
        response = jsonify(
            {
                "message": "User logged in successfully",
                "token": user_info["id_token"],
                "refresh_token": user_info['refresh_token'],
                "name": user_info["name"]
            }
        )
        response.status_code = 200
        return response
    except Exception as e:
        if "INVALID_LOGIN_CREDENTIALS" in str(e):
            return unauthorized("Invalid login credentials")
        elif "INVALID_PASSWORD" in str(e):
            return unauthorized("Invalid login credentials")
        elif "EMAIL_NOT_FOUND" in str(e):
            return unauthorized("Invalid login credentials")
        return forbidden(str(e))


def _check_user_data(data):
    required_fields = ["email", "password"]
    for field in required_fields:
        if field not in data:
            raise Exception(f"Missing required field {field}")
    return None


@bp.route("auth/refresh-token", methods=["POST"])
def refresh_token():
    try:
        data = request.get_json() or {}
        user_info = user_controller.refresh_token(data=data)
        response = jsonify(
            {"message": "Token refreshed successfully", "token": user_info["id_token"], "name": user_info["name"]}
        )
        response.status_code = 200
        return response
    except Exception as e:
        if "INVALID_REFRESH_TOKEN" in str(e):
            return unauthorized("Invalid refresh token")
        return forbidden(str(e))


def validate(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.headers.get("Authorization"):
            return forbidden("Missing token")
        try:
            user = auth.verify_id_token(request.headers["Authorization"])
            request.user = user
        except Exception:
            return unauthorized("Invalid token")
        return f(*args, **kwargs)

    return wrap


@bp.route("auth/reset-password", methods=["POST"])
def reset_password():
    try:
        data = request.get_json() or {}
        email = data.get("email")
        if not email:
            raise Exception("Missing required field email")
        response = user_controller.reset_password(email=email)
        response = jsonify(response)
        response.status_code = 200
        return response
    except Exception as e:
        return forbidden(str(e))


@bp.route("auth/verify-reset-token", methods=["POST"])
def verify_token():
    try:
        data = request.get_json() or {}
        token = data.get("token")
        if not token:
            raise Exception("Missing required field token")

        result = user_controller.verify_reset_token(token=token)

        if result.get("valid"):
            response = jsonify({"valid": True})
            response.status_code = 200
            return response
        else:
            return unauthorized(result.get("reason") or "Invalid token")
    except Exception as e:
        return forbidden(str(e))


@bp.route("auth/complete-reset-password", methods=["POST"])
def complete_reset_password():
    try:
        data = request.get_json() or {}
        token = data.get("token")
        new_password = data.get("password")

        if not token:
            raise Exception("Missing required field token")
        if not new_password:
            raise Exception("Missing required field password")

        result = user_controller.complete_reset_password(oob_code=token, new_password=new_password)
        response = jsonify({"message": "Password reset successfully"})
        response.status_code = 200
        return response
    except Exception as e:
        if "INVALID_OOB_CODE" in str(e):
            return unauthorized("Invalid or expired reset code")
        return forbidden(str(e))
