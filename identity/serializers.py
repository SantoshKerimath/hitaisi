from rest_framework import serializers
from .models import Organization, User


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'org_type', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'organization', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')

        # auto-fill username so Django is satisfied
        validated_data['username'] = validated_data['email']

        user = User(**validated_data)
        user.set_password(password)   # hashes password correctly
        user.save()
        return user
