from datetime import datetime
from app import db
from app.models import Activity
from app.controllers.user import users_collection


activities_collection = db.collection("activities")


def create_activities(data: dict):
    quantity = int(data.get("quantity"))
    created_time = data.get("created_time")
    if created_time:
        formatted_created_time = datetime.strptime(
            created_time, "%Y-%m-%dT%H:%M:%S.%fZ"
        )
    else:
        formatted_created_time = datetime.now().isoformat() + "Z"
    activities = []
    user_id = data.get("user_id")
    user_ref = users_collection.document(user_id)
    for _ in range(quantity):
        activity = Activity(
            user_ref=user_ref,
            activity_type=data.get("activity_type"),
            created_time=formatted_created_time,
        )
        activities_collection.add(activity.to_dict())
        activity.user_ref = user_ref.path
        activities.append(activity.to_dict())
    return activities


def get_activities(
    user_id: str, page: int = 1, per_page: int = 10, last_doc_id: str = None
):
    user_ref = users_collection.document(user_id)
    query = activities_collection.where("user_ref", "==", user_ref).order_by(
        "created_time"
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
    elif "user_id" in data:
        raise Exception("Cannot update user_id field")
    activity = activities_collection.document(activity_id).update(data)
    if not activity.to_dict():
        raise Exception("Activity not found")
    return activity.to_dict()


def delete_activity(activity_id: str):
    activity = activities_collection.document(activity_id).delete()
    if not activity.to_dict():
        raise Exception("Activity not found")
    return activity.to_dict()


def get_all_activities_per_type(
    user_id: str,
    start_date: str,
    end_date: str,
    page: int = 1,
    per_page: int = 10,
    last_doc_id: str = None,
):
    user_ref = users_collection.document(user_id)
    query = (
        activities_collection.where("user_ref", "==", user_ref)
        .where(
            "created_time", ">=", start_date,
        )
        .where(
            "created_time", "<=", end_date or datetime.now()
        )
        .order_by("created_time")
    )
    activities_list = _handle_pagination(
        query=query,
        page=page,
        per_page=per_page,
        last_doc_id=last_doc_id,
    )
    return activities_list


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
