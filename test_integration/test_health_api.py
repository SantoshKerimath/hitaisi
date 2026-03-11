import os
import requests

from test_integration.helpers import BASE_URL, INTEGRATION_TIMEOUT


def test_health_endpoint():

    assert BASE_URL

    response = requests.get(
        f"{BASE_URL}/health/",
        timeout=INTEGRATION_TIMEOUT,
    )

    assert response.status_code == 200