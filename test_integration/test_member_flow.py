import os
import requests

BASE_URL = os.getenv("BASE_URL")
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


def test_member_create():

    login = requests.post(
        f"{BASE_URL}/auth/login/",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        },
        timeout=10
    )

    assert login.status_code == 200

    token = login.json()["access"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        f"{BASE_URL}/member/create/",
        json={
            "name": "CI Test Employee",
            "age": 30
        },
        headers=headers,
        timeout=10
    )

    assert response.status_code in {200, 201}