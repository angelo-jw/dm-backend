import firebase_admin
import json
import pyrebase

from config import Config


def init_firebase():
    firebase = firebase_admin.initialize_app()
    return firebase


def init_pyrebase(config: Config):
    pb = pyrebase.initialize_app(json.load(open(config.FIREBASE_CONFIG_FILE)))
    return pb
