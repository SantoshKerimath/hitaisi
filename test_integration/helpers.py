import os
import requests

BASE_URL = os.getenv("BASE_URL")


def login_request(email: str, password: str, *, timeout: int = 10):
    return requests.post(
        f"{BASE_URL}/auth/login/",
        json={"email": email, "password": password},
        timeout=timeout,
    )


def create_ci_user(admin_token: str, *, timeout: int = 10):
    return requests.post(
        f"{BASE_URL}/users/create/",
        json={
            "email": "ci-test@tarkavada.com",
            "password": "CiPass123",
            "role": "org_admin",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
        timeout=timeout,
    )


def get_access_token(email: str, password: str, *, timeout: int = 10) -> str:
    response = login_request(email, password, timeout=timeout)
    assert response.status_code == 200, response.text
    return response.json()["access"]
