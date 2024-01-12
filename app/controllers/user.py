from app import db, auth_service
from app.models import User


users_collection = db.collection('users')


def create_user(data: dict):
    user = User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        state=data.get('state'),
    )
    user_cred = _handle_user_credentials(
        email=user.email,
        password=data.get('password'),
        full_name=user.full_name
    )
    user.id = user_cred.uid
    users_collection.document(user.id).set(user.to_dict())
    return user.to_dict()


def _handle_user_credentials(email, password, full_name):
    user_cred = auth_service.create_user(
            email=email,
            password=password,
            display_name=full_name,
    )
    return user_cred
