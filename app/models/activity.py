from dataclasses import dataclass
from datetime import datetime
from google.cloud.firestore_v1.document import DocumentReference


@dataclass()
class Activity:
    user_ref: DocumentReference
    activity_type: str
    created_time: datetime
    quantity: int

    def __repr__(self):
        return "<Activity {}>".format(self.activity_type)

    def to_dict(self) -> dict:
        data = {
            'user_ref': self.user_ref,
            'activity_type': self.activity_type,
            'created_time': self.created_time.isoformat() + 'Z',
            'quantity': self.quantity
        }
        return data

    def from_dict(self, data):
        for field in ["user_ref", "activity_type", "quantity", "created_time"]:
            if field in data:
                setattr(self, field, data[field])
