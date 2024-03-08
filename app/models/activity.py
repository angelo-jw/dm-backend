from dataclasses import dataclass
from google.cloud.firestore_v1.document import DocumentReference, Timestamp


@dataclass()
class Activity:
    user_ref: DocumentReference
    activity_type: str
    created_time: Timestamp
    quantity: int

    def __repr__(self):
        return "<Activity {}>".format(self.activity_type)

    def to_dict(self) -> dict:
        data = {
            'user_ref': self.user_ref,
            'activity_type': self.activity_type,
            'created_time': self.created_time,
            'quantity': self.quantity
        }
        return data

    def from_dict(self, data):
        for field in ["user_ref", "activity_type", "quantity", "created_time"]:
            if field in data:
                setattr(self, field, data[field])
