import pytest
import requests
from data import generate_email, generate_random_string, STANDARD_NAME_LENGTH, STANDARD_PASSWORD_LENGTH
from helpers import UserHelper, OrderHelper

@pytest.fixture
def random_user_data():
    return UserHelper.create_random_user_data()


@pytest.fixture
def random_registered_user_data():
    return UserHelper.register_user(UserHelper.create_random_user_data())


@pytest.fixture
def ingredients_ids():
    return OrderHelper.generate_order()

@pytest.fixture
def ingredients_invalid_ids():
    ids_src = OrderHelper.generate_order()
    invalid_ids = []
    for id in ids_src:
        invalid_ids.append(generate_random_string(len(id)))
    return invalid_ids


@pytest.fixture(scope="session", autouse=True)
def auto_delete_users():
    yield
    UserHelper.delete_all_users()
