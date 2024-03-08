from dataclasses import dataclass
import datetime
from google.cloud.firestore_v1.document import Timestamp


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    state: str
    created_time: Timestamp = datetime.datetime.now(tz=datetime.timezone.utc).replace(tzinfo=None)

    def __repr__(self):
        return '<User {}>'.format(self.full_name)

    def to_dict(self, include_email=False):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'state': self.state,
            'created_time': self.created_time
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['email', 'first_name', 'last_name', 'state']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
