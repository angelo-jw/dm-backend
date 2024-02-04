from datetime import datetime
from flask import jsonify, request

from app.api import bp
from app.api.auth import validate
from app.utils.errors import bad_request, not_found
from app.utils.tools import get_end_of_day
from app.controllers import activity as activity_controller


@bp.route("/activity", methods=["POST"])
@validate
def create_activity():
    try:
        data = request.get_json() or {}
        user_id = request.user.get("uid")
        data["user_id"] = user_id
        _check_activity_data(data)
        activities = activity_controller.create_activities(data=data)
        if len(activities) == 1:
            response = jsonify(
                {"message": "Activity created successfully", "activity": activities[0]}
            )
        else:
            response = jsonify(
                {"message": "Activities created successfully", "activities": activities}
            )
        response.status_code = 201
        return response
    except Exception as e:
        return bad_request(str(e))


def _check_activity_data(data):
    required_fields = ["activity_type", "quantity"]
    for field in required_fields:
        if field not in data:
            raise Exception(f"Missing required field {field}")
    return None


@bp.route("/activity/<activity_id>", methods=["GET"])
@validate
def get_activity(activity_id):
    try:
        activity = activity_controller.get_activity(activity_id=activity_id)
        response = jsonify({"activity": activity})
        response.status_code = 200
        return response
    except Exception as e:
        if "not found" in str(e):
            return not_found(str(e))
        return bad_request(str(e))


@bp.route("/activity", methods=["GET"])
@validate
def get_activities():
    try:
        user_id = request.user.get("uid")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        last_doc_id = request.args.get("last_doc_id")
        start_date = request.args.get("start_date")
        raw_end_date = request.args.get("end_date")
        if not raw_end_date:
            end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            end_date = get_end_of_day(raw_end_date)
        if not start_date:
            raise Exception("Missing required fields start_date")
        activities = activity_controller.get_activities(
            user_id=user_id,
            page=page,
            per_page=per_page,
            last_doc_id=last_doc_id,
            start_date=start_date,
            end_date=end_date
        )
        response = jsonify({"activities": activities})
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/activity/<activity_id>", methods=["PUT"])
@validate
def update_activity(activity_id):
    try:
        data = request.get_json() or {}
        message = activity_controller.update_activity(
            activity_id=activity_id, data=data
        )
        response = jsonify(
            {"message": message}
        )
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/activity/<activity_id>", methods=["DELETE"])
@validate
def delete_activity(activity_id):
    try:
        activity_controller.delete_activity(activity_id=activity_id)
        response = jsonify({"message": "Activity deleted successfully"})
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))
