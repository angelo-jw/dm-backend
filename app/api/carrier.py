from flask import jsonify, request

from app.api import bp
from app.api.auth import validate
from app.controllers import carrier as carrier_controller
from app.utils.errors import bad_request


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
        carriers_list = carrier_controller.get_carriers(
            user_id=user_id
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
