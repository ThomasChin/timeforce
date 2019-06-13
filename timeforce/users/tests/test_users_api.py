import json
import pytest
from rest_framework.test import APIClient

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
@pytest.mark.parametrize(
    "payload,expected",
    [
        (
            {"username": "lazydude", "email": "lazydude@lazy.com"},
            {"password": ["This field is required."]},
        ),
        (
            {"email": "lazydude2@lazy.com", "password": "lazydude2"},
            {"username": ["This field is required."]},
        ),
        (
            {"email": "lazydude3@lazy.com"},
            {"username": ["This field is required."], "password": ["This field is required."]},
        ),
    ],
)
def test_cannot_register_with_wrong_params(payload, expected):
    c = Client()
    r = c.post(f"{BASE_URL}/register", json.dumps(payload), "application/json")
    assert 400 == r.status_code


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


@pytest.mark.django_db
def test_login_with_non_registered_user_fails(unregistered_user_data):
    c = Client()
    payload = json.dumps(
        {
            "username": unregistered_user_data["username"],
            "password": unregistered_user_data["password"],
        }
    )
    r = c.post(f"{BASE_URL}/login", payload, "application/json")

    assert 400 == r.status_code


@pytest.mark.django_db
def test_retrieve_user_with_token(registered_user, registered_user_data):
    c = APIClient()
    payload = json.dumps(
        {"username": registered_user.username, "password": registered_user_data["password"]}
    )
    login_response = c.post(f"{BASE_URL}/login", payload, content_type="application/json")
    body = login_response.json()

    assert 200 == login_response.status_code
    assert {"user", "token"} == set(body.keys())

    token_header = f"Token {body['token']}"
    c.credentials(HTTP_AUTHORIZATION=token_header)
    get_user_response = c.get(f"{BASE_URL}/user", {}, content_type="application/json")
    body = get_user_response.json()

    assert 200 == get_user_response.status_code
    assert {"id", "username", "email"} == set(body.keys())
    assert registered_user.id == body["id"]
    assert registered_user.username == body["username"]
    assert registered_user.email == body["email"]


@pytest.mark.django_db
def test_retrieve_user_without_token_fails(registered_user, registered_user_data):
    c = APIClient()
    payload = json.dumps(
        {"username": registered_user.username, "password": registered_user_data["password"]}
    )
    login_response = c.post(f"{BASE_URL}/login", payload, content_type="application/json")
    body = login_response.json()

    assert 200 == login_response.status_code
    assert {"user", "token"} == set(body.keys())

    get_user_response = c.get(f"{BASE_URL}/user", {}, content_type="application/json")

    assert 401 == get_user_response.status_code


@pytest.mark.django_db
def test_retrieve_user_with_invalid_token_fails(registered_user, registered_user_data):
    c = APIClient()
    payload = json.dumps(
        {"username": registered_user.username, "password": registered_user_data["password"]}
    )
    login_response = c.post(f"{BASE_URL}/login", payload, content_type="application/json")
    body = login_response.json()

    assert 200 == login_response.status_code
    assert {"user", "token"} == set(body.keys())

    token_header = f"Something {body['token']}"
    c.credentials(HTTP_AUTHORIZATION=token_header)
    get_user_response = c.get(f"{BASE_URL}/user", {}, content_type="application/json")

    assert 401 == get_user_response.status_code


@pytest.mark.django_db
def test_logout_with_token(registered_user, registered_user_data):
    c = APIClient()
    payload = json.dumps(
        {"username": registered_user.username, "password": registered_user_data["password"]}
    )
    login_response = c.post(f"{BASE_URL}/login", payload, content_type="application/json")
    body = login_response.json()

    assert 200 == login_response.status_code
    assert {"user", "token"} == set(body.keys())
    token_header = f"Token {body['token']}"
    c.credentials(HTTP_AUTHORIZATION=token_header)
    get_user_response = c.post(f"{BASE_URL}/logout", content_type="application/json")

    assert 204 == get_user_response.status_code


@pytest.mark.django_db
def test_logout_without_token_fails(registered_user, registered_user_data):
    c = APIClient()
    payload = json.dumps(
        {"username": registered_user.username, "password": registered_user_data["password"]}
    )
    login_response = c.post(f"{BASE_URL}/login", payload, content_type="application/json")
    body = login_response.json()

    assert 200 == login_response.status_code
    assert {"user", "token"} == set(body.keys())

    get_user_response = c.post(f"{BASE_URL}/logout", content_type="application/json")
    assert 401 == get_user_response.status_code


@pytest.mark.django_db
def test_token_invalidates_after_logout(registered_user, registered_user_data):
    c = APIClient()
    payload = json.dumps(
        {"username": registered_user.username, "password": registered_user_data["password"]}
    )
    login_response = c.post(f"{BASE_URL}/login", payload, content_type="application/json")
    body = login_response.json()

    assert 200 == login_response.status_code
    assert {"user", "token"} == set(body.keys())
    token_header = f"Token {body['token']}"
    c.credentials(HTTP_AUTHORIZATION=token_header)
    get_user_response = c.post(f"{BASE_URL}/logout", content_type="application/json")
    assert 204 == get_user_response.status_code

    get_user_response = c.get(f"{BASE_URL}/user", {}, content_type="application/json")
    assert 401 == get_user_response.status_code
