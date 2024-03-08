from datetime import datetime

from app import db
from app.models import Carrier
from app.controllers.user import users_collection


carriers_collection = db.collection("carriers")


class CarrierAlreadyExistError(Exception):
    pass


def create_carriers(data: dict):
    created_time = datetime.utcnow()
    user_id = data.get("user_id")
    user_ref = users_collection.document(user_id)
    carrier_name = data.get("carrier_name")
    _carrier_exists = get_carrier_by_name(carrier_name, user_ref=user_ref)
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


def get_carrier_by_name(carrier_name: str, user_ref: str):
    carrier = carriers_collection.where("carrier_name", "==", carrier_name).where(
        "user_ref", "==", user_ref
    ).stream()
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
):
    user_ref = users_collection.document(user_id)
    query = (
        carriers_collection.where("user_ref", "==", user_ref)
        .order_by("created_time")
    )
    carriers_list = []
    for carrier in query.stream():
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
