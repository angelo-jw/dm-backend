from dataclasses import dataclass
from google.cloud.firestore_v1.document import DocumentReference


@dataclass()
class ActivityType:
    user_ref: DocumentReference
    name: str
    duration: int

    def __repr__(self):
        return "<Activity {}>".format(self.activity_type)

    def to_dict(self) -> dict:
        data = {
            'user_ref': self.user_ref,
            'name': self.name,
            'duration': self.duration
        }
        return data

    def from_dict(self, data):
        for field in ["user_ref", "name", "duration"]:
            if field in data:
                setattr(self, field, data[field])
