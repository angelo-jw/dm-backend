from dataclasses import dataclass
from datetime import datetime
from google.cloud.firestore_v1.document import DocumentReference


@dataclass()
class Payment:
    user_ref: DocumentReference
    created_time: datetime
    amount: float
    created_time: datetime
    carrier_ref: DocumentReference
    door_knock_commission: bool

    def __repr__(self):
        return "<Payment {}>".format(self.amount)

    def to_dict(self) -> dict:
        data = {
            "user_ref": self.user_ref,
            "amount": self.amount,
            "created_time": self.created_time.isoformat() + "Z",
            "carrier_ref": self.carrier_ref,
            "door_knock_commission": self.door_knock_commission,
        }
        return data

    def from_dict(self, data):
        for field in [
            "user_ref",
            "created_time",
            "amount",
            "carrier_ref",
            "door_knock_commission",
        ]:
            if field in data:
                setattr(self, field, data[field])
