import requests


BASE_URL = "https://tarkavada.com"


def test_health_endpoint():
    response = requests.get(f"{BASE_URL}/api/v1/health/")

    assert response.status_code == 200