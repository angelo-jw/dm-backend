from faker import Faker
import pytest

fake = Faker()


@pytest.fixture
def test_user():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password": fake.pystr(min_chars=8, max_chars=16),
        "state": fake.state()
    }
