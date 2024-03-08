from flask import jsonify, request

from app.api import bp
from app.api.auth import validate
from app.utils.errors import bad_request
from app.utils.tools import format_dates_for_api
from app.controllers import activity as activity_controller
from app.controllers import deposit as deposit_controller


@bp.route("/get-activity-count", methods=["GET"])
@validate
def get_activity_count_by_date_range():
    try:
        user_id = request.user.get("uid")
        raw_start_date = request.args.get("start_date")
        if not raw_start_date:
            raise Exception("Missing required fields start_date")
        raw_end_date = request.args.get("end_date")
        start_date, end_date = format_dates_for_api(raw_start_date, raw_end_date)
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


@bp.route("/get-sales-by-weekday", methods=["GET"])
@validate
def get_sales_by_weekday():
    try:
        user_id = request.user.get("uid")
        raw_start_date = request.args.get("start_date")
        if not raw_start_date:
            raise Exception("Missing required fields start_date")
        raw_end_date = request.args.get("end_date")
        start_date, end_date = format_dates_for_api(raw_start_date, raw_end_date)
        sales_by_weekday = deposit_controller.get_sales_by_weekday(
            user_id=user_id, start_date=start_date, end_date=end_date
        )
        response = jsonify(sales_by_weekday)
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))


@bp.route("/get-sales-per-activity", methods=["GET"])
@validate
def get_sales_per_activity():
    try:
        user_id = request.user.get("uid")
        raw_start_date = request.args.get("start_date")
        if not raw_start_date:
            raise Exception("Missing required fields start_date")
        raw_end_date = request.args.get("end_date")
        start_date, end_date = format_dates_for_api(raw_start_date, raw_end_date)
        sales_per_activity = deposit_controller.get_sales_per_activity(
            user_id=user_id, start_date=start_date, end_date=end_date
        )
        response = jsonify(sales_per_activity)
        response.status_code = 200
        return response
    except Exception as e:
        return bad_request(str(e))
