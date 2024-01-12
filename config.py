import dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv.load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    FIREBASE_CONFIG_FILE = os.environ.get("FIREBASE_CONFIG_FILE") or "firebase-config-test.json"
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or "test"
    ENV = os.environ.get("ENV") or "test"
