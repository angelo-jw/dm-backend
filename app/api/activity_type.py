from flask import jsonify, request

from app.api import bp
from app.api.auth import validate
from app.utils.errors import bad_request, not_found
from app.controllers import activity_type as activity_type_controller


@bp.route("/activity-type", methods=["POST"])
@validate
def create_activity_type():
    try:
        data = request.get_json() or {}
        user_id = request.user.get("uid")
        data["user_id"] = user_id
        _check_activity_type_data(data)
        created_activity_type = activity_type_controller.create_activity_types(data=data)
        response = jsonify(
            {
                "message": "activity_type created successfully",
                "activity_type": created_activity_type,
            }
        )
        response.status_code = 201
        return response
    except Exception as e:
        return bad_request(str(e))


def _check_activity_type_data(data):
    required_fields = ["name", "duration"]
    for field in required_fields:
        if field not in data:
            raise Exception(f"Missing required field {field}")
    return None


@bp.route("/activity-type/<activity_type_id>", methods=["GET"])
@validate
def get_activity_type(activity_type_id):
    try:
        activity_type = activity_type_controller.get_activity_type(activity_type_id=activity_type_id)
        response = jsonify({"activity_type": activity_type})
        response.status_code = 200
        return response
    except Exception as e:
        if "not found" in str(e):
            return not_found(str(e))
        return bad_request(str(e))


@bp.route("/activity-type", methods=["GET"])
@validate
def get_activity_types():
    try:
        user_id = request.user.get("uid")
        activity_types = activity_type_controller.get_activity_types(
            user_id=user_id,
        )
        response = jsonify({"activity_types": activity_types})
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/activity-type/<activity_type_id>", methods=["PUT"])
@validate
def update_activity_type(activity_type_id):
    try:
        data = request.get_json() or {}
        message = activity_type_controller.update_activity_type(
            activity_type_id=activity_type_id, data=data
        )
        response = jsonify({"message": message})
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/activity-type/<activity_type_id>", methods=["DELETE"])
@validate
def delete_activity_type(activity_type_id):
    try:
        activity_type_controller.delete_activity_type(activity_type_id=activity_type_id)
        response = jsonify({"message": "activity_type deleted successfully"})
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))
