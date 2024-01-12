import firebase_admin
import json
import pyrebase

from flask import Flask
from flask_cors import CORS

from app.services.auth import init_auth_service
from app.services.firebase import init_firebase, init_pyrebase
from app.services.database import init_db

from config import Config


def init_services():
    config_class = Config
    firebase = init_firebase()
    pb = init_pyrebase(config=config_class)
    auth_service = init_auth_service(config=config_class)
    db = init_db(config=config_class, client=firebase)

    return firebase, pb, auth_service, db


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


firebase, pb, auth_service, db = init_services()


from app import models  # noqa:E402
