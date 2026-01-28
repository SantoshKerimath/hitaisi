from benefits.models import PremiumRate

def calculate_member_premium(member):
    rate = PremiumRate.objects.filter(
        product=member.policy.product,
        relation=member.relation,
        min_age__lte=member.age,
        max_age__gte=member.age,
        sum_insured=member.sum_insured
    ).first()

    if not rate:
        raise ValueError("No premium rate configured for this demographic")

    return rate.annual_premium