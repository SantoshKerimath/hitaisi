import os
import requests
from test_integration.helpers import create_ci_user, get_access_token

BASE_URL = os.getenv("BASE_URL")
ADMIN_EMAIL = os.getenv("TEST_EMAIL")
ADMIN_PASSWORD = os.getenv("TEST_PASSWORD")


def test_member_create():

    admin_token = get_access_token(ADMIN_EMAIL, ADMIN_PASSWORD)

    create_ci_user(admin_token)

    token = get_access_token("ci-test@tarkavada.com", "CiPass123")

    response = requests.post(
        f"{BASE_URL}/member/create/",
        json={
            "name": "CI Test Employee",
            "age": 30
        },
        headers={"Authorization": f"Bearer {token}"},
        timeout=10
    )

    assert response.status_code in {200, 201}