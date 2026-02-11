import pytest
from rest_framework.test import APIClient
from datetime import date, timedelta
from identity.models import Organization, User
from benefits.models import (
    Client, Product, Policy,
    PremiumRate, PremiumBuffer
)

@pytest.mark.django_db
def test_employee_add_and_delete_dependent():

    # Setup org + HR
    org = Organization.objects.create(name="Employer", org_type="employer")
    hr = User.objects.create(
        email="hr@test.com",
        username="hr",
        role="org_admin",
        organization=org
    )
    hr.set_password("Hr@123")
    hr.save()

    client_obj = Client.objects.create(name="Client", organization=org)
    product = Product.objects.create(name="Product", base_sum_insured=500000)

    PremiumRate.objects.create(
        product=product,
        relation="employee",
        min_age=18,
        max_age=60,
        sum_insured=500000,
        annual_premium=10000
    )

    PremiumRate.objects.create(
        product=product,
        relation="spouse",
        min_age=18,
        max_age=60,
        sum_insured=500000,
        annual_premium=8000
    )

    today = date.today()
    policy = Policy.objects.create(
        policy_number="POL1",
        client=client_obj,
        product=product,
        status="issued",
        start_date=today,
        end_date=today + timedelta(days=365)
    )

    PremiumBuffer.objects.create(policy=policy)
    
    api_client = APIClient()

    login = api_client.post(
        "/api/auth/login/",
        {"email": "hr@test.com", "password": "Hr@123"},
        format="json"
    )

    token = login.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # Add Employee first (via API)
    response = api_client.post(
        "/api/members/",
        {
            "policy": policy.id,
            "name": "John",
            "relation": "employee",
            "employee_code": "EMP1",
            "date_of_birth": "1990-01-01",
            "gender": "male",
            "age": 34,
            "sum_insured": 500000,
            "cover_start_date": str(today),
            "cover_end_date": str(today + timedelta(days=365))
        },
        format="json"
    )

    assert response.status_code == 201

    # NOW employee user exists
    employee_user = User.objects.get(email="emp1@member.local")
    employee_user.set_password("Emp@123")
    employee_user.save()

    api_client = APIClient()
    login = api_client.post(
        "/api/auth/login/",
        {
            "email": employee_user.email,
            "password": "Emp@123"
        },
        format="json"
    )
    token = login.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # Add spouse dependent
    response = api_client.post(
        "/api/member/dependents/add/",
        {
            "policy": policy.id,
            "name": "Jane",
            "relation": "spouse",
            "employee_code": "EMP1",
            "date_of_birth": "1992-01-01",
            "gender": "female",
            "age": 32,
            "sum_insured": 500000,
            "cover_start_date": str(today),
            "cover_end_date": str(today + timedelta(days=365))
        },
        format="json"
    )

    assert response.status_code == 201

    buffer = PremiumBuffer.objects.get(policy=policy)
    assert buffer.premium_used == 18000
