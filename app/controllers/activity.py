from datetime import datetime
from collections import defaultdict
from google.cloud.firestore_v1.base_query import FieldFilter

from app import db
from app.models import Activity
from app.controllers.user import users_collection
from app.utils.tools import parse_iso_datetime


activities_collection = db.collection("activities")


def create_activities(data: dict):
    quantity = int(data.get("quantity"))
    created_time = data.get("created_time")
    if created_time:
        date_obj = datetime.strptime(
            created_time, "%Y-%m-%d"
        )
        current_time = datetime.now()
        formatted_created_time = date_obj.replace(
            hour=current_time.hour,
            minute=current_time.minute,
            second=current_time.second,
            microsecond=current_time.microsecond,
        )
    else:
        formatted_created_time = datetime.now()
    user_id = data.get("user_id")
    user_ref = users_collection.document(user_id)
    activity = Activity(
            user_ref=user_ref,
            activity_type=data.get("activity_type"),
            created_time=formatted_created_time,
            quantity=quantity
    )
    activities_collection.add(activity.to_dict())
    activity.user_ref = user_ref.path
    return activity.to_dict()


def get_activities(
    user_id: str,
    start_date: str,
    end_date: str,
    page: int = 1,
    per_page: int = 10,
    last_doc_id: str = None,
):
    user_ref = users_collection.document(user_id)
    query = (
        activities_collection.where(filter=FieldFilter("user_ref", "==", user_ref))
        .where(filter=FieldFilter("created_time", ">=", start_date))
        .where(filter=FieldFilter("created_time", "<=", end_date))
        .order_by("created_time")
    )
    activities_list = _handle_pagination(
        query=query,
        page=page,
        per_page=per_page,
        last_doc_id=last_doc_id,
    )

    return activities_list


def get_activity(activity_id: str):
    activity = activities_collection.document(activity_id).get()
    activity_dict = activity.to_dict()
    if not activity_dict:
        raise Exception("Activity not found")
    activity_dict["user_ref"] = activity_dict["user_ref"].id
    activity_dict["id"] = activity.id
    return activity_dict


def update_activity(activity_id: str, data: dict):
    if "id" in data:
        raise Exception("Cannot update id field")
    if "user_id" in data:
        raise Exception("Cannot update user_id field")
    activities_collection.document(activity_id).update(data)
    return "Activity updated successfully"


def delete_activity(activity_id: str):
    activities_collection.document(activity_id).delete()
    return "Activity deleted successfully"


def _handle_pagination(query, page, per_page, last_doc_id):
    if last_doc_id and page > 1:
        last_doc = activities_collection.document(last_doc_id).get()
        if not last_doc.exists:
            raise Exception("Last document not found")
        query = query.start_after(last_doc)

    activities = query.limit(per_page).stream()
    activities_list = []
    for activity in activities:
        activity_dict = activity.to_dict()
        activity_dict["user_ref"] = activity_dict["user_ref"].id
        activity_dict["id"] = activity.id
        activities_list.append(activity_dict)
    return activities_list


def get_activity_count_by_date_range(user_id: str, start_date: str, end_date: str):
    user_ref = users_collection.document(user_id)
    query = (
        activities_collection.where(filter=FieldFilter("user_ref", "==", user_ref))
        .where(filter=FieldFilter("created_time", ">=", start_date))
        .where(filter=FieldFilter("created_time", "<=", end_date))
        .stream()
    )
    activities_by_date = defaultdict(int)
    for activity in query:
        activity_data = activity.to_dict()
        activity_type = activity_data["activity_type"]
        quantity = int(activity_data["quantity"])
        activities_by_date[activity_type] += quantity
    formatted_activities = dict(activities_by_date)
    return formatted_activities


def get_activity_count_per_month(user_id: str, year: str):
    user_ref = users_collection.document(user_id)
    query = (
        activities_collection.where(filter=FieldFilter("user_ref", "==", user_ref))
        .where(filter=FieldFilter("created_time", ">=", f"{year}-01-01T00:00:00.000Z"))
        .where(filter=FieldFilter("created_time", "<=", f"{year}-12-31T23:59:59.999Z"))
        .stream()
    )
    activities_by_month = defaultdict(lambda: defaultdict(int))
    for activity in query:
        activity_data = activity.to_dict()
        created_datetime = parse_iso_datetime(activity_data["created_time"])
        month_key = created_datetime.strftime("%Y-%m")
        activity_type = activity_data["activity_type"]
        quantity = int(activity_data["quantity"])
        activities_by_month[month_key][activity_type] += quantity
    formatted_activities = {
        month: dict(activities) for month, activities in activities_by_month.items()
    }
    return formatted_activities
