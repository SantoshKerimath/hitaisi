import os
from test_integration.helpers import create_ci_user, get_access_token

BASE_URL = os.getenv("BASE_URL")
ADMIN_EMAIL = os.getenv("TEST_EMAIL")
ADMIN_PASSWORD = os.getenv("TEST_PASSWORD")

def test_login():

    admin_token = get_access_token(ADMIN_EMAIL, ADMIN_PASSWORD, timeout=10)

    create_ci_user(admin_token)

    _ = get_access_token("ci-test@tarkavada.com", "CiPass123", timeout=10)