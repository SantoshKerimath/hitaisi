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
    if response.status_code != 200:
        # Common production/CI failure mode: secrets point to a user that doesn't exist or is inactive.
        hint = ""
        try:
            body = response.json()
            if isinstance(body, dict) and body.get("detail") == "No active account found with the given credentials":
                hint = (
                    "\n\nHint: The deployed API rejected TEST_EMAIL/TEST_PASSWORD. "
                    "Verify the GitHub Secrets values match an existing *active* user "
                    "in the deployed environment."
                )
        except Exception:
            pass

        raise AssertionError(
            f"Login failed: {response.status_code} {response.text}{hint}"
        )
    return response.json()["access"]
