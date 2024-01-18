import json
import requests
from firebase_admin import auth

from app import db
from app.models import User
from app.utils import endpoints, constants


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
    user_cred = auth.create_user(
            email=email,
            password=password,
            display_name=full_name,
    )
    return user_cred


def login(data: dict):
    url = endpoints.IDENTITY_TOOLKIT + 'accounts:signInWithPassword?key=' + constants.API_KEY
    payload = {
        "email": data.get('email'),
        "password": data.get('password'),
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    _raise_detailed_error(response)
    return response.json().get('idToken')


def _raise_detailed_error(request_object):
    try:
        request_object.raise_for_status()
    except requests.HTTPError:
        text = request_object.text.find("{")
        parsed_text = json.loads(request_object.text[text:])
        raise requests.HTTPError(parsed_text.get('error').get('message'))
