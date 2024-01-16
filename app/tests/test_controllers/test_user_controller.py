import pytest
from firebase_admin._auth_utils import EmailAlreadyExistsError

import app.controllers.user as user_controller


def test__create_user__returns_user__when_user_does_not_exist(test_user, db_session):
    created_user = user_controller.create_user(test_user)

    assert created_user['email'] == test_user['email']


def test__create_user__returns_none__when_email_already_exists(test_user, db_session):
    user_controller.create_user(test_user)
    with pytest.raises(EmailAlreadyExistsError) as excinfo:
        user_controller.create_user(test_user)
    assert excinfo.value.code == 'ALREADY_EXISTS'


def test__create_user__returns_none__when_email_is_invalid(test_user, db_session):
    test_user['email'] = 'invalid_email'
    with pytest.raises(ValueError) as excinfo:
        user_controller.create_user(test_user)
    assert excinfo.value.args[0] == 'Malformed email address string: "invalid_email".'
