import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FIRESTORE_EMULATOR_HOST = os.environ.get("FIRESTORE_EMULATOR_HOST")
    FIRESTORE_AUTH_EMULATOR_HOST = os.environ.get("FIRESTORE_AUTH_EMULATOR_HOST")
    FIRESTORE_URL = os.environ.get("FIRESTORE_URL")
    AUTH_URL = os.environ.get("AUTH_URL")
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    QUOTA_PROJECT_ID = os.environ.get("QUOTA_PROJECT_ID")
    REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")
    TYPE = os.environ.get("TYPE")
    IDENTITY_TOOLKIT_URL = os.environ.get("IDENTITY_TOOLKIT_URL")
    API_KEY = os.environ.get("API_KEY")
