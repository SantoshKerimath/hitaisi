import os
import requests
from test_integration.helpers import create_ci_user, get_access_token, INTEGRATION_TIMEOUT

BASE_URL = os.getenv("BASE_URL")
ADMIN_EMAIL = os.getenv("TEST_EMAIL")
ADMIN_PASSWORD = os.getenv("TEST_PASSWORD")


def test_member_create():

    admin_token = get_access_token(ADMIN_EMAIL, ADMIN_PASSWORD, timeout=INTEGRATION_TIMEOUT)

    create_ci_user(admin_token, timeout=INTEGRATION_TIMEOUT)

    token = get_access_token("ci-test@tarkavada.com", "CiPass123", timeout=INTEGRATION_TIMEOUT)

    response = requests.post(
        f"{BASE_URL}/member/create/",
        json={
            "name": "CI Test Employee",
            "age": 30
        },
        headers={"Authorization": f"Bearer {token}"},
        timeout=INTEGRATION_TIMEOUT,
    )

    assert response.status_code in {200, 201}