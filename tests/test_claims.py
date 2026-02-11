import pytest
from datetime import date, timedelta
from identity.models import Organization, User
from benefits.models import Client, Product, Policy, Member
from claims.models import Claim

@pytest.mark.django_db
def test_claim_creation():

    org = Organization.objects.create(
        name="Employer",
        org_type="employer"
    )

    client_obj = Client.objects.create(
        name="Client",
        organization=org
    )

    product = Product.objects.create(
        name="Product",
        base_sum_insured=500000
    )

    policy = Policy.objects.create(
        policy_number="POLC1",
        client=client_obj,
        product=product,
        status="issued",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=365)
    )

    member = Member.objects.create(
        policy=policy,
        name="John",
        relation="employee",
        employee_code="EMP100",
        date_of_birth="1990-01-01",
        gender="male",
        age=34,
        sum_insured=500000,
        cover_start_date=date.today(),
        cover_end_date=date.today() + timedelta(days=365),
        premium=10000
    )

    claim = Claim.objects.create(
        policy=policy,
        member=member,
        claim_number="CLM001",
        status="submitted"
    )

    assert claim.status == "submitted"
