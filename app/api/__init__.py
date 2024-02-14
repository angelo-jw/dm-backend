from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import user, auth, activity, dashboard, carrier, deposit  # noqa:E402, F401
