import pytest
from rest_framework.test import APIClient
from identity.models import Organization, User
from benefits.models import Client, Product, Policy
from tickets.models import SupportTicket
from datetime import date, timedelta

@pytest.mark.django_db
def test_ticket_creation():

    org = Organization.objects.create(name="Employer", org_type="employer")
    user = User.objects.create(
        email="user@test.com",
        username="user",
        role="org_admin",
        organization=org
    )
    user.set_password("Test@123")
    user.save()

    client_obj = Client.objects.create(name="Client", organization=org)
    product = Product.objects.create(name="Prod", base_sum_insured=500000)

    policy = Policy.objects.create(
        policy_number="POL2",
        client=client_obj,
        product=product,
        status="issued",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=365)
    )

    api_client = APIClient()
    login = api_client.post(
        "/api/auth/login/",
        {"email": "user@test.com", "password": "Test@123"},
        format="json"
    )
    token = login.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = api_client.post(
        "/api/tickets/create/",
        {
            "policy": policy.id,
            "subject": "Policy Issue",
            "assigned_to_role": "ops_user"
        },
        format="json"
    )

    assert response.status_code == 201
    assert SupportTicket.objects.count() == 1
    
