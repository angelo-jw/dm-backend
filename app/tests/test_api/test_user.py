import pytest
from faker import Faker

fake = Faker()


def test__create_user__returns_201__when_valid_data(test_client, test_user):
    user = test_user

    response = test_client.post('/api/users', json=user)

    assert response.status_code == 201


@pytest.mark.parametrize('field', ['first_name', 'last_name', 'email', 'state'])
def test__create_user__returns_bad_request__when_missing_data(test_client, test_user, field):
    user = test_user
    del user[field]

    response = test_client.post('/api/users', json=user)

    assert response.status_code == 400
    assert f'Missing required field {field}' in response.json['message']


def test__create_user_returns_bad_request__when_duplicate_email(test_client, test_user, user_factory, mocker):
    user = user_factory(**test_user)

    test_client.post('/api/users', json=user)
    response = test_client.post('/api/users', json=user)

    assert response.status_code == 400
    assert 'The user with the provided email already exists (EMAIL_EXISTS).' in response.json['message']
