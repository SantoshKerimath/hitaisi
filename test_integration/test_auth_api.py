import os
import requests

BASE_URL = os.getenv("BASE_URL")
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


def test_login():

    assert BASE_URL
    assert TEST_EMAIL
    assert TEST_PASSWORD

    response = requests.post(
        f"{BASE_URL}/auth/login/",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        },
        timeout=10
    )

    if response.status_code != 200:
        print(response.text)

    assert response.status_code == 200

    data = response.json()

    assert "access" in data
    assert "refresh" in data