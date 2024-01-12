from dataclasses import dataclass
from faker import Faker
from firebase_admin import auth

from config import Config


@dataclass
class MockUserCred:
    uid: str
    email: str
    password: str
    display_name: str
    disabled: bool = False
    email_verified: bool = False


class MockAuthService:
    def create_user(self, email, password, display_name):
        _email_exists = self.verify_email_exists(email)
        if _email_exists:
            raise Exception("The user with the provided email already exists (EMAIL_EXISTS).")
        return MockUserCred(
            uid=Faker().uuid4(),
            email=email,
            password=password,
            display_name=display_name
        )

    def verify_email_exists(self, email):
        from app import db
        users = list(db.collection("users").where("email", "==", email).get())
        return len(users) > 0


def init_auth_service(config: Config):
    if config.ENV == "test":
        return MockAuthService()
    else:
        return auth
