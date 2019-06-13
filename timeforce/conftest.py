import pytest
import json

from django.contrib.auth.models import User
from knox.models import AuthToken


@pytest.fixture()
def unregistered_user_data():
    return {"username": "chargebolt", "email": "kaminari@ua.com", "password": "stungun"}


@pytest.fixture()
def registered_user_data():
    return {"username": "earphonejack", "email": "jirou@ua.com", "password": "rock70"}


@pytest.fixture()
def registered_user(registered_user_data):
    user = User.objects.create_user(
        registered_user_data["username"],
        registered_user_data["email"],
        registered_user_data["password"],
    )
    token = AuthToken.objects.create(user)[1]

    return user
