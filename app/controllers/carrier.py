from datetime import datetime

from app import db
from app.models import Carrier
from app.controllers.user import users_collection


carriers_collection = db.collection("carriers")


class CarrierAlreadyExistError(Exception):
    pass


def create_carriers(data: dict):
    created_time = datetime.now()
    user_id = data.get("user_id")
    user_ref = users_collection.document(user_id)
    carrier_name = data.get("carrier_name")
    _carrier_exists = get_carrier_by_name(carrier_name)
    if _carrier_exists:
        message = "Carrier already exists"
        raise CarrierAlreadyExistError(message)
    carrier = Carrier(
        user_ref=user_ref,
        carrier_name=carrier_name,
        created_time=created_time,
        notes=data.get("notes"),
    )
    carriers_collection.add(carrier.to_dict())
    carrier.user_ref = user_ref.path
    return carrier.to_dict()


def get_carrier_by_name(carrier_name: str):
    carrier = carriers_collection.where("carrier_name", "==", carrier_name).stream()
    return [doc.to_dict() for doc in carrier]


def get_carrier(carrier_id: str):
    carrier = carriers_collection.document(carrier_id).get()
    carrier_dict = carrier.to_dict()
    if not carrier_dict:
        raise Exception("Carrier not found")
    carrier_dict["user_ref"] = carrier_dict["user_ref"].id
    carrier_dict["id"] = carrier.id
    return carrier_dict


def get_carriers(
    user_id: str,
    start_date: str,
    end_date: str,
    page: int = 1,
    per_page: int = 10,
    last_doc_id: str = None,
):
    user_ref = users_collection.document(user_id)
    query = (
        carriers_collection.where("user_ref", "==", user_ref)
        .where("created_time", ">=", start_date)
        .where("created_time", "<=", end_date)
        .order_by("created_time")
    )
    carriers_list = _handle_pagination(
        query=query,
        page=page,
        per_page=per_page,
        last_doc_id=last_doc_id,
    )
    return carriers_list


def _handle_pagination(query, page, per_page, last_doc_id):
    if last_doc_id and page > 1:
        last_doc = carriers_collection.document(last_doc_id).get()
        if not last_doc.exists:
            raise Exception("Last document not found")
        query = query.start_after(last_doc)

    carriers = query.limit(per_page).stream()
    carriers_list = []
    for carrier in carriers:
        carrier_dict = carrier.to_dict()
        carrier_dict["user_ref"] = carrier_dict["user_ref"].id
        carrier_dict["id"] = carrier.id
        carriers_list.append(carrier_dict)
    return carriers_list


def update_carrier(carrier_id: str, data: dict):
    if "id" in data:
        raise Exception("Cannot update id field")
    if "user_id" in data:
        raise Exception("Cannot update user_id field")
    carriers_collection.document(carrier_id).update(data)
    return "Carrier updated successfully"


def delete_carrier(carrier_id: str):
    carriers_collection.document(carrier_id).delete()
    return "Carrier deleted successfully"
