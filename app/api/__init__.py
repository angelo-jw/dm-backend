from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import user, auth, activity, dashboard, carrier, payment  # noqa:E402, F401
