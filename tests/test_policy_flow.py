import pytest
from django.urls import reverse
from benefits.models import PremiumRate, PremiumBuffer


@pytest.mark.django_db
def test_member_add_updates_premium_buffer(hr_client, base_policy, base_product):

    PremiumRate.objects.create(
        product=base_product,
        relation="employee",
        min_age=18,
        max_age=60,
        sum_insured=500000,
        annual_premium=12000
    )

    member_url = reverse("member-create")

    response = hr_client.post(
        member_url,
        {
            "policy": base_policy.id,
            "name": "John",
            "relation": "employee",
            "employee_code": "EMP100",
            "date_of_birth": "1990-01-01",
            "gender": "male",
            "age": 34,
            "sum_insured": 500000,
            "cover_start_date": str(base_policy.start_date),
            "cover_end_date": str(base_policy.end_date)
        },
        format="json"
    )

    assert response.status_code == 201

    buffer = PremiumBuffer.objects.get(policy=base_policy)
    assert buffer.premium_used == 12000
