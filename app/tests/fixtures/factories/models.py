import pytest
from faker import Faker
from app.models import User


@pytest.fixture
def user_collection(db_session):
    return db_session.collection('users')


@pytest.fixture
def user_factory(user_collection):
    def create_user(**kwargs):
        user = User(
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name'),
            email=kwargs.get('email'),
            state=kwargs.get('state')
        )
        user.id = Faker().uuid4()
        user_collection.document(user.id).set(user.to_dict())
        users = list(user_collection.limit(4).get())
        test_user = user.to_dict()
        test_user['password'] = kwargs['password']
        return test_user

    return create_user
