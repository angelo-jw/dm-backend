from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import user  # noqa:E402, F401
