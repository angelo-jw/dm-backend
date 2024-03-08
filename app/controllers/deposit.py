from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

from app import db
from app.models import Deposit
from app.controllers.activity import get_activity_count_by_date_range
from app.controllers.carrier import carriers_collection, get_carrier
from app.controllers.user import users_collection


deposit_colletion = db.collection("deposits")


def create_deposit(data: dict):
    created_time = data.get("created_time")
    if created_time:
        date_obj = datetime.strptime(
            created_time, "%Y-%m-%d"
        )
        current_time = datetime.utcnow()
        formatted_created_time = date_obj.replace(
            hour=current_time.hour,
            minute=current_time.minute,
            second=current_time.second,
            microsecond=current_time.microsecond,
        )
    else:
        formatted_created_time = datetime.utcnow()
    user_id = data.get("user_id")
    user_ref = users_collection.document(user_id)
    carrier_ref = carriers_collection.document(data.get("carrier_id"))
    deposit = Deposit(
        user_ref=user_ref,
        amount=float(data.get("amount")),
        created_time=formatted_created_time,
        carrier_ref=carrier_ref,
        door_knock_commission=data.get("door_knock_commission"),
    )
    deposit_colletion.add(deposit.to_dict())
    deposit.user_ref = user_ref.path
    deposit.carrier_ref = carrier_ref.path
    return deposit.to_dict()


def get_deposit(deposit_id: str):
    deposit = deposit_colletion.document(deposit_id).get()
    deposit_dict = deposit.to_dict()
    if not deposit_dict:
        raise Exception("Deposit not found")
    deposit_dict["user_ref"] = deposit_dict["user_ref"].id
    deposit_dict["carrier_ref"] = deposit_dict["carrier_ref"].id
    deposit_dict["id"] = deposit.id
    return deposit_dict


def get_deposits(
    user_id: str,
    start_date: str,
    end_date: str,
    page: int = 1,
    per_page: int = 10,
    last_doc_id: str = None,
):
    user_ref = users_collection.document(user_id)
    datetime_obj = DatetimeWithNanoseconds
    start_date = datetime_obj.from_rfc3339(start_date)
    end_date = datetime_obj.from_rfc3339(end_date)
    query = (
        deposit_colletion.where(filter=FieldFilter("user_ref", "==", user_ref))
        .where(filter=FieldFilter("created_time", ">=", start_date))
        .where(filter=FieldFilter("created_time", "<=", end_date))
        .order_by("created_time")
    )
    deposits_list = _handle_pagination(
        query=query,
        page=page,
        per_page=per_page,
        last_doc_id=last_doc_id,
    )
    return deposits_list


def _handle_pagination(query, page, per_page, last_doc_id):
    if last_doc_id and page > 1:
        last_doc = deposit_colletion.document(last_doc_id).get()
        if not last_doc.exists:
            raise Exception("Last document not found")
        query = query.start_after(last_doc)

    deposits = query.limit(per_page).stream()
    deposits_list = []
    for deposit in deposits:
        deposit_dict = deposit.to_dict()
        deposit_dict["user_ref"] = deposit_dict["user_ref"].id
        deposit_dict["carrier_ref"] = deposit_dict["carrier_ref"].id
        carrier_name = get_carrier(deposit_dict["carrier_ref"]).get("carrier_name")
        deposit_dict["carrier_name"] = carrier_name
        deposit_dict["id"] = deposit.id
        deposits_list.append(deposit_dict)
    return deposits_list


def update_deposit(deposit_id: str, data: dict):
    if "id" in data:
        raise Exception("Cannot update id field")
    if "user_id" in data:
        raise Exception("Cannot update user_id field")
    if "carrier_id" in data:
        data["carrier_ref"] = carriers_collection.document(data.get("carrier_id"))
        data.pop("carrier_id")
    deposit_colletion.document(deposit_id).update(data)
    return "Deposit updated successfully"


def delete_deposit(deposit_id: str):
    deposit_colletion.document(deposit_id).delete()
    return "Deposit deleted successfully"


def get_sales_by_weekday(user_id: str, start_date: str, end_date: str):
    user_ref = users_collection.document(user_id)
    datetime_obj = DatetimeWithNanoseconds
    start_date = datetime_obj.from_rfc3339(start_date)
    end_date = datetime_obj.from_rfc3339(end_date)
    query = (
        deposit_colletion.where(filter=FieldFilter("user_ref", "==", user_ref))
        .where(filter=FieldFilter("created_time", ">=", start_date))
        .where(filter=FieldFilter("created_time", "<=", end_date))
    )
    deposits = query.stream()
    sales_by_weekday = {
        "Monday": 0,
        "Tuesday": 0,
        "Wednesday": 0,
        "Thursday": 0,
        "Friday": 0,
        "Saturday": 0,
        "Sunday": 0,
    }
    for deposit in deposits:
        deposit_dict = deposit.to_dict()
        created_time = deposit_dict.get("created_time")
        weekday = created_time.strftime("%A")
        sales_by_weekday[weekday] += int(deposit_dict.get("amount"))
    return sales_by_weekday


def get_sales_per_activity(user_id: str, start_date: str, end_date: str):
    user_ref = users_collection.document(user_id)
    activity_counts = get_activity_count_by_date_range(start_date=start_date, end_date=end_date, user_id=user_id)
    datetime_obj = DatetimeWithNanoseconds
    start_date = datetime_obj.from_rfc3339(start_date)
    end_date = datetime_obj.from_rfc3339(end_date)
    query = (
        deposit_colletion.where(filter=FieldFilter("user_ref", "==", user_ref))
        .where(filter=FieldFilter("created_time", ">=", start_date))
        .where(filter=FieldFilter("created_time", "<=", end_date))
    )
    deposits = query.stream()
    total_deposits = sum(deposit.to_dict()['amount'] for deposit in deposits)
    door_knock_commission_total = 0

    for deposit in deposits:
        deposit_data = deposit.to_dict()
        total_deposits += deposit_data['amount']
        if deposit_data.get('door_knock_commission'):
            door_knock_commission_total += deposit_data['amount']

    sales_per_activity_type = {}
    for activity_type, count in activity_counts.items():
        if count > 0:
            if activity_type == "DoorKnocks":
                sales_per_activity_type[activity_type] = round(door_knock_commission_total / count, 2)
            else:
                sales_per_activity_type[activity_type] = round(total_deposits / count, 2)

    return sales_per_activity_type
