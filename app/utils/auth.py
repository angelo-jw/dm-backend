from functools import wraps
from flask import request, jsonify
from firebase_admin import auth


def validate(f):
    """
    A decorator to verify a firebase ID token from the Authorization header
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        id_token = None

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith('Bearer '):
            id_token = auth_header.split('Bearer ')[1]

        if not id_token:
            response = jsonify({"message": "Authorization token is missing or invalid."})
            response.status_code = 401
            return response
        
        try:
            decoded_token = auth.verify_id_token(id_token)
            request.user = decoded_token
        except auth.InvalidIdTokenError:
            response = jsonify({"message": "Invalid token."})
            response.status_code = 401
            return response
        except Exception as e:
            response = jsonify({"message": f"Error verifying token: {str(e)}"})
            response.status_code = 500
            return response

        return f(*args, **kwargs)
    
    return decorated_function