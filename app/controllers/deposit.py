from datetime import datetime

from app import db
from app.models import Deposit
from app.controllers.user import users_collection
from app.controllers.carrier import carriers_collection, get_carrier


deposit_colletion = db.collection("deposits")


def create_deposit(data: dict):
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
    carrier_ref = carriers_collection.document(data.get("carrier_id"))
    deposit = Deposit(
        user_ref=user_ref,
        amount=data.get("amount"),
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
    query = (
        deposit_colletion.where("user_ref", "==", user_ref)
        .where("created_time", ">=", start_date)
        .where("created_time", "<=", end_date)
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
