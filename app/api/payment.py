from datetime import datetime
from flask import jsonify, request

from app.api import bp
from app.api.auth import validate
from app.controllers import payment as payment_controller
from app.utils.tools import get_end_of_day
from app.utils.errors import bad_request


@bp.route("/payment", methods=["POST"])
@validate
def create_payment():
    try:
        data = request.get_json() or {}
        user_id = request.user.get("uid")
        data["user_id"] = user_id
        _check_payment_data(data)
        payment_controller.create_payment(data=data)
        response = jsonify({"message": "Payment created successfully"})
        response.status_code = 201
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/payment/<payment_id>", methods=["GET"])
@validate
def get_payment(payment_id):
    try:
        payment = payment_controller.get_payment(payment_id=payment_id)
        response = jsonify({"payment": payment})
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/payment", methods=["GET"])
@validate
def get_payments():
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
        payments_list = payment_controller.get_payments(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            page=page,
            per_page=per_page,
            last_doc_id=last_doc_id,
        )
        response = jsonify({"payments": payments_list})
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/payment/<payment_id>", methods=["PUT"])
@validate
def update_payment(payment_id):
    try:
        data = request.get_json() or {}
        response = payment_controller.update_payment(
            payment_id=payment_id, data=data
        )
        response = jsonify(
            {"message": response}
        )
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/payment/<payment_id>", methods=["DELETE"])
@validate
def delete_payment(payment_id):
    try:
        payment_controller.delete_payment(payment_id=payment_id)
        response = jsonify({"message": "Payment deleted successfully"})
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


def _check_payment_data(data: dict):
    required_fields = ["amount", "carrier_id", "door_knock_commission"]
    for field in required_fields:
        if field not in data:
            raise Exception(f"Missing required field {field}")
    return None
