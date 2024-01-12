import pytest
import secrets

from app import create_app

from .fixtures import *  # noqa F401, F403


@pytest.fixture
def test_app():
    flask_app = create_app()
    flask_app.app_context().push()
    flask_app.secret_key = secrets.token_urlsafe(32)

    yield flask_app

    flask_app.app_context().pop()


@pytest.fixture
def test_client(test_app):
    client = test_app.test_client()
    return client


@pytest.fixture
def db_session(test_app):
    from app import db
    with test_app.app_context():
        yield db
        db.reset()
