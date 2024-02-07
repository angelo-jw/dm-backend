from datetime import datetime

from app import db
from app.models import Payment
from app.controllers.user import users_collection
from app.controllers.carrier import carriers_collection, get_carrier


payment_colletion = db.collection("payments")


def create_payment(data: dict):
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
    payment = Payment(
        user_ref=user_ref,
        amount=data.get("amount"),
        created_time=formatted_created_time,
        carrier_ref=carrier_ref,
        door_knock_commission=data.get("door_knock_commission"),
    )
    payment_colletion.add(payment.to_dict())
    payment.user_ref = user_ref.path
    payment.carrier_ref = carrier_ref.path
    return payment.to_dict()


def get_payment(payment_id: str):
    payment = payment_colletion.document(payment_id).get()
    payment_dict = payment.to_dict()
    if not payment_dict:
        raise Exception("Payment not found")
    payment_dict["user_ref"] = payment_dict["user_ref"].id
    payment_dict["carrier_ref"] = payment_dict["carrier_ref"].id
    payment_dict["id"] = payment.id
    return payment_dict


def get_payments(
    user_id: str,
    start_date: str,
    end_date: str,
    page: int = 1,
    per_page: int = 10,
    last_doc_id: str = None,
):
    user_ref = users_collection.document(user_id)
    query = (
        payment_colletion.where("user_ref", "==", user_ref)
        .where("created_time", ">=", start_date)
        .where("created_time", "<=", end_date)
        .order_by("created_time")
    )
    payments_list = _handle_pagination(
        query=query,
        page=page,
        per_page=per_page,
        last_doc_id=last_doc_id,
    )
    return payments_list


def _handle_pagination(query, page, per_page, last_doc_id):
    if last_doc_id and page > 1:
        last_doc = payment_colletion.document(last_doc_id).get()
        if not last_doc.exists:
            raise Exception("Last document not found")
        query = query.start_after(last_doc)

    payments = query.limit(per_page).stream()
    payments_list = []
    for payment in payments:
        payment_dict = payment.to_dict()
        payment_dict["user_ref"] = payment_dict["user_ref"].id
        payment_dict["carrier_ref"] = payment_dict["carrier_ref"].id
        carrier_name = get_carrier(payment_dict["carrier_ref"]).get("carrier_name")
        payment_dict["carrier_name"] = carrier_name
        payment_dict["id"] = payment.id
        payments_list.append(payment_dict)
    return payments_list


def update_payment(payment_id: str, data: dict):
    if "id" in data:
        raise Exception("Cannot update id field")
    if "user_id" in data:
        raise Exception("Cannot update user_id field")
    if "carrier_id" in data:
        data["carrier_ref"] = carriers_collection.document(data.get("carrier_id"))
        data.pop("carrier_id")
    payment_colletion.document(payment_id).update(data)
    return "Payment updated successfully"


def delete_payment(payment_id: str):
    payment_colletion.document(payment_id).delete()
    return "Payment deleted successfully"
