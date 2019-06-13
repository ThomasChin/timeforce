import json
import pytest

from django.test import Client

BASE_URL = "/api/auth"


@pytest.mark.django_db
def test_register_view():
    username = "ironman"
    email = "tony@stark.com"
    password = "loveu3000"

    payload = json.dumps({"username": username, "email": email, "password": password})

    c = Client()

    r = c.post(f"{BASE_URL}/register", payload, "application/json")
    assert 200 == r.status_code
    assert {"user", "token"} == set(r.json().keys())
