import json
import pytest

from django.test import Client

BASE_URL = "/api/auth"


@pytest.mark.django_db
def test_register_new_user():
    username = "ironman"
    email = "tony@stark.com"
    password = "loveu3000"

    payload = json.dumps({"username": username, "email": email, "password": password})

    c = Client()

    r = c.post(f"{BASE_URL}/register", payload, "application/json")
    assert 200 == r.status_code
    assert {"user", "token"} == set(r.json().keys())


@pytest.mark.django_db
def test_login_with_new_user():
    c = Client()
    username = "ironman"
    email = "tony@stark.com"
    password = "loveu3000"

    register_payload = json.dumps({"username": username, "email": email, "password": password})
    register_response = c.post(f"{BASE_URL}/register", register_payload, "application/json")

    assert 200 == register_response.status_code
    assert {"user", "token"} == set(register_response.json().keys())

    login_payload = json.dumps({"username": username, "password": password})
    login_response = c.post(f"{BASE_URL}/login", login_payload, "application/json")

    assert 200 == login_response.status_code
    assert {"user", "token"} == set(login_response.json().keys())


# TODO: Test Login with non-registered fails
@pytest.mark.django_db
def test_login_with_non_registered_user_fails():
    c = Client()


# TODO: Test register fails without right payload params

# TODO: Test Get User w/ Token works

# TODO: Test Get User w/o Token doesn't work

# TODO: Test Get User w/ invalid Token doesn't work

# TODO: Test Logout works w/ token

# TODO: Test logout w/out token doesn't work
