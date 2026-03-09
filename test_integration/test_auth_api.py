import os
import requests

BASE_URL = os.getenv("BASE_URL", "https://tarkavada.com/api/v1")
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


def test_login():

    assert TEST_EMAIL is not None
    assert TEST_PASSWORD is not None

    response = requests.post(
        f"{BASE_URL}/auth/login/",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access" in data
    assert "refresh" in data