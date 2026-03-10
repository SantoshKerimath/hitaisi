import pytest
from datetime import date, timedelta
from django.urls import reverse
from rest_framework.test import APIClient
from identity.models import Organization, User
from benefits.models import Client, Product, Policy, PremiumBuffer


# ---------- Base Org ----------
@pytest.fixture
def employer_org():
    return Organization.objects.create(
        name="Test Employer",
        org_type="employer"
    )


# ---------- HR User ----------
@pytest.fixture
def hr_user(employer_org):
    user = User.objects.create(
        email="hr@test.com",
        username="hr",
        role="org_admin",
        organization=employer_org
    )
    user.set_password("Hr@123")
    user.save()
    return user


# ---------- Authenticated Client ----------
@pytest.fixture
def hr_client(hr_user):
    client = APIClient()
    login_url = reverse("token_obtain_pair")

    response = client.post(
        login_url,
        {"email": "hr@test.com", "password": "Hr@123"},
        format="json"
    )

    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    return client


# ---------- Base Product ----------
@pytest.fixture
def base_product():
    return Product.objects.create(
        name="Base Product",
        base_sum_insured=500000
    )


# ---------- Base Policy ----------
@pytest.fixture
def base_policy(employer_org, base_product):
    client_obj = Client.objects.create(
        name="Test Client",
        organization=employer_org
    )

    today = date.today()

    policy = Policy.objects.create(
        policy_number="POL001",
        client=client_obj,
        product=base_product,
        status="issued",
        start_date=today,
        end_date=today + timedelta(days=365)
    )

    PremiumBuffer.objects.create(policy=policy)

    return policy


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, hr_user):

    login_url = reverse("token_obtain_pair")

    response = api_client.post(
        login_url,
        {
            "email": "hr@test.com",
            "password": "Hr@123"
        },
        format="json"
    )

    token = response.data["access"]

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    return api_client