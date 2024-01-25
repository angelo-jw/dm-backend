import os
import base64
import json

from firebase_admin import initialize_app, firestore, credentials
from flask import Flask
from flask_cors import CORS

from config import Config

encoded_credentials = os.environ.get("GOOGLE_CREDENTIALS")
decoded_credentials = base64.b64decode(encoded_credentials)
firebase_credential = credentials.Certificate(json.loads(decoded_credentials))
firebase = initialize_app(firebase_credential)
db = firestore.client()


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


from app import models  # noqa:E402
