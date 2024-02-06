from datetime import datetime
from flask import jsonify, request

from app.api import bp
from app.api.auth import validate
from app.controllers import carrier as carrier_controller
from app.utils.errors import bad_request
from app.utils.tools import get_end_of_day


@bp.route("/carrier", methods=["POST"])
@validate
def create_carrier():
    try:
        data = request.get_json() or {}
        user_id = request.user.get("uid")
        data["user_id"] = user_id
        carrier_controller.create_carriers(data=data)
        response = jsonify(
            {"message": "Carrier created successfully"}
        )
        response.status_code = 201
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/carrier/<carrier_id>", methods=["GET"])
@validate
def get_carrier(carrier_id):
    try:
        carrier = carrier_controller.get_carrier(carrier_id=carrier_id)
        response = jsonify({"carrier": carrier})
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/carrier", methods=["GET"])
@validate
def get_carriers():
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
        carriers_list = carrier_controller.get_carriers(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            page=page,
            per_page=per_page,
            last_doc_id=last_doc_id,
        )
        response = jsonify({"carriers": carriers_list})
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/carrier/<carrier_id>", methods=["PUT"])
@validate
def update_carrier(carrier_id):
    try:
        data = request.get_json() or {}
        carrier_controller.update_carrier(carrier_id=carrier_id, data=data)
        response = jsonify(
            {"message": "Carrier updated successfully"}
        )
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/carrier/<carrier_id>", methods=["DELETE"])
@validate
def delete_carrier(carrier_id):
    try:
        carrier_controller.delete_carrier(carrier_id=carrier_id)
        response = jsonify(
            {"message": "Carrier deleted successfully"}
        )
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))
