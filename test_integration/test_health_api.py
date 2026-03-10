import os
import requests

BASE_URL = os.getenv("BASE_URL")


def test_health_endpoint():

    assert BASE_URL

    response = requests.get(
        f"{BASE_URL}/health/",
        timeout=10
    )

    assert response.status_code == 200