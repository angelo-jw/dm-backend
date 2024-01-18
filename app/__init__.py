from firebase_admin import initialize_app, firestore
from flask import Flask
from flask_cors import CORS

from config import Config


firebase = initialize_app()
db = firestore.client()


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


from app import models  # noqa:E402
