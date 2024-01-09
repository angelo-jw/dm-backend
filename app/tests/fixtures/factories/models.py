import pytest
from app.models import User


@pytest.fixture
def user_factory(db_session):
    def create_user(**kwargs):
        user = User(**kwargs)
        try:
            db_session.add(user)
            db_session.commit()
        finally:
            db_session.rollback()
        test_user = user.to_dict()
        test_user['password'] = kwargs['password_hash']
        test_user.pop('id')
        return test_user

    return create_user
