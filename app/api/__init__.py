from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import user, auth, activity, dashboard, carrier, deposit, activity_type  # noqa:E402, F401
