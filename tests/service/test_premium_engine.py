import pytest
from benefits.models import Product, PremiumRate
from benefits.services.premium_engine import calculate_member_premium
from benefits.models import Member, Policy, Client
from identity.models import Organization
from datetime import date, timedelta

@pytest.mark.django_db
def test_premium_engine_calculation():

    org = Organization.objects.create(name="Test", org_type="employer")
    client = Client.objects.create(name="Client", organization=org)
    product = Product.objects.create(name="Prod", base_sum_insured=500000)

    PremiumRate.objects.create(
        product=product,
        relation="employee",
        min_age=18,
        max_age=60,
        sum_insured=500000,
        annual_premium=15000
    )

    today = date.today()
    policy = Policy.objects.create(
        policy_number="T1",
        client=client,
        product=product,
        status="issued",
        start_date=today,
        end_date=today + timedelta(days=365)
    )

    member = Member.objects.create(
        policy=policy,
        name="John",
        relation="employee",
        employee_code="EMP1",
        date_of_birth=date(1990,1,1),
        gender="male",
        age=34,
        sum_insured=500000,
        cover_start_date=today,
        cover_end_date=today + timedelta(days=365)
    )

    premium = calculate_member_premium(member)
    assert premium == 15000
