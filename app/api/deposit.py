from datetime import datetime
from flask import jsonify, request

from app.api import bp
from app.api.auth import validate
from app.controllers import deposit as deposit_controller
from app.utils.tools import get_end_of_day
from app.utils.errors import bad_request


@bp.route("/deposit", methods=["POST"])
@validate
def create_deposit():
    try:
        data = request.get_json() or {}
        user_id = request.user.get("uid")
        data["user_id"] = user_id
        _check_deposit_data(data)
        deposit_controller.create_deposit(data=data)
        response = jsonify({"message": "Deposit created successfully"})
        response.status_code = 201
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/deposit/<deposit_id>", methods=["GET"])
@validate
def get_deposit(deposit_id):
    try:
        deposit = deposit_controller.get_deposit(deposit_id=deposit_id)
        response = jsonify({"deposit": deposit})
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/deposit", methods=["GET"])
@validate
def get_deposits():
    try:
        user_id = request.user.get("uid")
        start_date = request.args.get("start_date")
        if not start_date:
            raise Exception("Missing required fields start_date")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        last_doc_id = request.args.get("last_doc_id")
        raw_end_date = request.args.get("end_date")
        if not raw_end_date:
            end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            end_date = get_end_of_day(raw_end_date)
        deposits_list = deposit_controller.get_deposits(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            page=page,
            per_page=per_page,
            last_doc_id=last_doc_id,
        )
        response = jsonify({"deposits": deposits_list})
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/deposit/<deposit_id>", methods=["PUT"])
@validate
def update_deposit(deposit_id):
    try:
        data = request.get_json() or {}
        response = deposit_controller.update_deposit(
            deposit_id=deposit_id, data=data
        )
        response = jsonify(
            {"message": response}
        )
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/deposit/<deposit_id>", methods=["DELETE"])
@validate
def delete_deposit(deposit_id):
    try:
        deposit_controller.delete_deposit(deposit_id=deposit_id)
        response = jsonify({"message": "Deposit deleted successfully"})
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


def _check_deposit_data(data: dict):
    required_fields = ["amount", "carrier_id", "door_knock_commission"]
    for field in required_fields:
        if field not in data:
            raise Exception(f"Missing required field {field}")
    return None
