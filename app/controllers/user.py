import logging
import json
import requests
from firebase_admin import auth

from app import db
from app.models import User
from app.utils import endpoints, constants


users_collection = db.collection('users')
logger = logging.getLogger(__name__)


def create_user(data: dict):
    user = User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        state=data.get('state'),
    )
    user_cred = auth.create_user(
            email=user.email,
            password=data.get('password'),
            display_name=user.full_name,
    )
    user.id = user_cred.uid
    try:
        from app.controllers.activity_type import create_default_activity_types
        users_collection.document(user.id).set(user.to_dict())
        create_default_activity_types(user.id)
    except Exception as e:
        # auth.delete_user(user_cred.uid)
        # print(e)
        # raise Exception("User creation failed")
        logger.error(f"User creation failed, rolling back. Error: {e}")
        auth.delete_user(user_cred.uid)
        raise e
    return user.to_dict()


def get_user_by_id(uid: str):
    """Gets a user by their UID from firestore"""
    user_doc = users_collection.document(uid).get()
    if user_doc.exists:
        return user_doc.to_dict()
    return None


def update_user(uid: str, data: dict):
    """updates a user's data in firestore"""
    users_collection.document(uid).update(data)


def login(data: dict):
    url = endpoints.IDENTITY_TOOLKIT + 'accounts:signInWithPassword?key=' + constants.API_KEY
    payload = {
        "email": data.get('email'),
        "password": data.get('password'),
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    _raise_detailed_error(response)
    id_token = response.json().get('idToken')
    refresh_token = response.json().get('refreshToken')
    data = {
        "id_token": id_token,
        "refresh_token": refresh_token,
        "name": _get_user_info_from_id_token(id_token).get('name')
    }
    return data


def _raise_detailed_error(request_object):
    try:
        request_object.raise_for_status()
    except requests.HTTPError:
        text = request_object.text.find("{")
        parsed_text = json.loads(request_object.text[text:])
        raise requests.HTTPError(parsed_text.get('error').get('message'))


def _get_user_info_from_id_token(id_token):
    decoded_token = auth.verify_id_token(id_token)
    return decoded_token


def refresh_token(data: dict):
    url = endpoints.GOOGLE_SECURE_TOKEN_URL + 'token?key=' + constants.API_KEY
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": data.get('refresh_token')
    }
    response = requests.post(url, json=payload)
    _raise_detailed_error(response)
    id_token = response.json().get('id_token')
    data = {
        "id_token": id_token,
        "name": _get_user_info_from_id_token(id_token).get('name')
    }
    return data


def reset_password(email: str):
    import re
    from app.utils.emails import send_password_reset_email
    try:
        full_reset_link = auth.generate_password_reset_link(email)

        oob_match = re.search(r'oobCode=([^&]+)', full_reset_link)
        if oob_match:
            oob_code = oob_match.group(1)
            send_password_reset_email(email, oob_code)

            if constants.ENVIRONMENT == 'development':
                return {
                    "message": "Password reset email sent",
                    "oob_code": oob_code,
                }
            return {"message": "Password reset email sent successfully"}
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        raise Exception("Error sending password reset email")


def verify_reset_token(token: str):
    try:

        url = f"{endpoints.IDENTITY_TOOLKIT}accounts:resetPassword?key={constants.API_KEY}"
        payload = {"oobCode": token}

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            return {"valid": True}
        else:
            return {"valid": False, "reason": "Invalid or expired token"}
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return {"valid": False, "reason": str(e)}


def complete_reset_password(oob_code: str, new_password: str):
    """Process actual password reset with the oobCode and new password"""
    try:
        url = f"{endpoints.IDENTITY_TOOLKIT}accounts:resetPassword?key={constants.API_KEY}"
        payload = {
            "oobCode": oob_code,
            "newPassword": new_password
        }
        response = requests.post(url, json=payload)
        _raise_detailed_error(response)
        return {"success": True}
    except Exception as e:
        logger.error(f"Error completing reset: {str(e)}")
        raise
