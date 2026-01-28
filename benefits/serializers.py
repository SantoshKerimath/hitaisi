from rest_framework import serializers
from django.utils.crypto import get_random_string
from .models import (
    Client, Product, ProductCoverage,
    Policy, PolicyCoverage, Member,
    PolicyDocument, PremiumBuffer
)
from identity.models import User
from benefits.services.premium_engine import calculate_member_premium



class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'organization', 'created_at']


class ProductCoverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCoverage
        fields = ['id', 'coverage_name', 'is_covered', 'has_sublimit', 'sublimit_amount']


class ProductSerializer(serializers.ModelSerializer):
    coverages = ProductCoverageSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'base_sum_insured', 'coverages', 'created_at']

    def create(self, validated_data):
        coverages_data = validated_data.pop('coverages')
        product = Product.objects.create(**validated_data)
        for cov in coverages_data:
            ProductCoverage.objects.create(product=product, **cov)
        return product


class PolicyCoverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyCoverage
        fields = ['coverage_name', 'is_covered', 'sublimit_amount']


class PolicySerializer(serializers.ModelSerializer):
    policy_coverages = PolicyCoverageSerializer(many=True, read_only=True)

    class Meta:
        model = Policy
        fields = [
            'id', 'policy_number', 'client', 'product',
            'status', 'start_date', 'end_date',
            'policy_coverages', 'created_at'
        ]

class PolicyStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['draft', 'issued', 'in_force'])



class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            'id', 'policy', 'name', 'relation', 'employee_code',
            'date_of_birth', 'gender', 'age', 'sum_insured',
            'cover_start_date', 'cover_end_date'
        ]

    def create(self, validated_data):
        policy = validated_data['policy']

        # Default cover dates if not supplied
        cover_start = validated_data.get('cover_start_date') or policy.start_date
        cover_end = validated_data.get('cover_end_date') or policy.end_date

        member = Member.objects.create(
            **validated_data,
            cover_start_date=cover_start,
            cover_end_date=cover_end
        )

        # Ensure buffer exists
        buffer, _ = PremiumBuffer.objects.get_or_create(policy=policy)

        # Calculate premium
        premium_amount = calculate_member_premium(member)
        member.premium = premium_amount
    
        # Update ledger
        buffer.premium_used += premium_amount
        buffer.recalc()

        # Create login only for employee
        if member.relation == 'employee':
            temp_password = get_random_string(8)
            user = User.objects.create(
                email=f"{member.employee_code.lower()}@member.local",
                username=f"mem_{member.id}",
                role='member_user',
                organization=policy.client.organization
            )
            user.set_password(temp_password)
            user.save()
            member.user = user
            print(f"Member login created: {user.email} / {temp_password}")
        
        member.save()
        return member



class PolicyDocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = PolicyDocument
        fields = ['id', 'policy', 'title', 'file', 'uploaded_at']


def validate(self, data):
    exists = Member.objects.filter(
        policy=data['policy'],
        employee_code=data['employee_code'],
        name__iexact=data['name'],
        date_of_birth=data['date_of_birth']
    ).exists()

    if exists:
        raise serializers.ValidationError(
            "This member already exists under this employee_code in this policy."
        )

    return data