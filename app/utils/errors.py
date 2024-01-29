from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    return error_response(400, message=message)


def unauthorized(message):
    return error_response(401, message=message)


def forbidden(message):
    return error_response(403, message=message)


def not_found(message):
    return error_response(404, message=message)
