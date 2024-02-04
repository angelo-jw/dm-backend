from dataclasses import dataclass
from datetime import datetime
from google.cloud.firestore_v1.document import DocumentReference


@dataclass()
class Carrier:
    user_ref: DocumentReference
    carrier_name: str
    created_time: datetime
    notes: str

    def __repr__(self):
        return "<Carrier {}>".format(self.carrier_name)

    def to_dict(self) -> dict:
        data = {
            'user_ref': self.user_ref,
            'carrier_name': self.carrier_name,
            'created_time': self.created_time.isoformat() + 'Z',
            'notes': self.notes
        }
        return data

    def from_dict(self, data):
        for field in ["user_ref", "carrier_name", "notes", "created_time"]:
            if field in data:
                setattr(self, field, data[field])
