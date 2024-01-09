from faker import Faker
import pytest

fake = Faker()


@pytest.fixture
def test_user():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password_hash": fake.word(),
        "state": fake.state()
    }
