import pytest
from datetime import date, timedelta
from rest_framework.test import APIClient
from identity.models import User, Organization
from benefits.models import Policy, Client, Product, PremiumBuffer, PremiumRate


@pytest.mark.django_db
def test_member_add_updates_premium_buffer():
    # Create org
    org = Organization.objects.create(
        name="Test Employer",
        org_type="employer"
    )

    # Create HR user
    hr = User.objects.create(
        email="hr@test.com",
        username="hr",
        role="org_admin",
        organization=org
    )
    hr.set_password("Hr@123")
    hr.save()

    # Create client
    client_obj = Client.objects.create(
        name="Test Client",
        organization=org
    )

    # Create product
    product = Product.objects.create(
        name="Test Product",
        base_sum_insured=500000
    )


    PremiumRate.objects.create(
        product=product,
        relation="employee",
        min_age=18,
        max_age=60,
        sum_insured=500000,
        annual_premium=12000
    )

    # Create policy
    today = date.today()
    one_year_later = today + timedelta(days=365)
    policy = Policy.objects.create(
        policy_number="POL123",
        client=client_obj,
        product=product,
        status="issued",
        start_date=today,
        end_date=one_year_later
    )


    PremiumBuffer.objects.create(policy=policy)

    # Login
    api_client = APIClient()
    login = api_client.post(
        "/api/auth/login/",
        {"email": "hr@test.com", "password": "Hr@123"},
        format="json"
    )

    token = login.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # Add member
    response = api_client.post(
        "/api/members/",
        {
            "policy": policy.id,
            "name": "John Employee",
            "relation": "employee",
            "employee_code": "EMP100",
            "date_of_birth": "1990-01-01",
            "gender": "male",
            "age": 34,
            "sum_insured": 500000,
            "cover_start_date": str(today),
            "cover_end_date": str(one_year_later)
        },
        format="json"
    )


    assert response.status_code == 201

    buffer = PremiumBuffer.objects.get(policy=policy)
    assert buffer.premium_used == 12000

