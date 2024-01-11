import firebase_admin
import json
import pyrebase

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from firebase_admin import credentials, firestore

from config import Config


#db = SQLAlchemy()
#migrate = Migrate()
firebase_cred = credentials.Certificate('firebase-key.json')
firebase = firebase_admin.initialize_app(firebase_cred)
pb = pyrebase.initialize_app(json.load(open('firebase-config.json')))
db = firestore.client(firebase)


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)
    # db.init_app(app)
    # migrate.init_app(app, db)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


from app import models  # noqa:E402
