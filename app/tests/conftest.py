import pytest
import requests
import secrets

from app import create_app
from config import Config

from .fixtures import *  # noqa F401, F403


def clear_firebase():
    firestore_url = Config.FIRESTORE_URL
    auth_url = Config.AUTH_URL
    requests.delete(firestore_url)
    requests.delete(auth_url)


@pytest.fixture
def test_app():
    flask_app = create_app()
    flask_app.app_context().push()
    flask_app.secret_key = secrets.token_urlsafe(32)

    yield flask_app

    clear_firebase()


@pytest.fixture
def test_client(test_app):
    client = test_app.test_client()
    return client


@pytest.fixture
def db_session(test_app):
    from app import db
    with test_app.app_context():
        yield db
    clear_firebase()
