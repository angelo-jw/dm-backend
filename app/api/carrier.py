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
