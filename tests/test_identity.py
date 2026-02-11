import pytest
from rest_framework.test import APIClient
from identity.models import Organization, User


@pytest.mark.django_db
def test_platform_admin_login():
    org = Organization.objects.create(
        name="HITAISI",
        org_type="insurer"
    )

    admin = User.objects.create(
        email="admin@hitaisi.com",
        username="admin",
        role="platform_admin",
        organization=org
    )
    admin.set_password("Admin@123")
    admin.save()

    client = APIClient()

    response = client.post(
        "/api/auth/login/",
        {
            "email": "admin@hitaisi.com",
            "password": "Admin@123"
        },
        format="json"
    )

    assert response.status_code == 200
    assert "access" in response.data
