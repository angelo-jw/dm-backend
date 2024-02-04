from datetime import datetime
from flask import jsonify, request

from app.api import bp
from app.api.auth import validate
from app.utils.errors import bad_request
from app.utils.tools import get_end_of_day
from app.controllers import activity as activity_controller


@bp.route("/get-activity-count", methods=["GET"])
@validate
def get_activity_count_by_date_range():
    try:
        user_id = request.user.get("uid")
        start_date = request.args.get("start_date")
        if not start_date:
            raise Exception("Missing required fields start_date")
        raw_end_date = request.args.get("end_date")
        if not raw_end_date:
            end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            end_date = get_end_of_day(raw_end_date)
        activities_dict_per_day = activity_controller.get_activity_count_by_date_range(
            user_id=user_id, start_date=start_date, end_date=end_date
        )
        response = jsonify(activities_dict_per_day)
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/get-activity-count-per-month", methods=["GET"])
@validate
def get_activity_count_per_month():
    try:
        user_id = request.user.get("uid")
        year = request.args.get("year")
        if not year:
            raise Exception("Missing required fields year")
        activities_dict_per_month = activity_controller.get_activity_count_per_month(
            user_id=user_id, year=year
        )
        response = jsonify(activities_dict_per_month)
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))
