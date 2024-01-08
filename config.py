import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    IS_DEV = os.environ.get("IS_DEV") or "True"
    API_KEY = os.environ.get("API_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") if not \
        IS_DEV else "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_KEY = os.environ.get("JWT_KEY")
    JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
