from django.db import models
from django.contrib.auth.models import AbstractUser


class Organization(models.Model):
    ORG_TYPES = [
        ('employer', 'Employer'),
        ('broker', 'Broker'),
        ('insurer', 'Insurer'),
        ('tpa', 'TPA'),
    ]

    name = models.CharField(max_length=255)
    org_type = models.CharField(max_length=20, choices=ORG_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_TYPES = [
        ('platform_admin', 'Platform Admin'),
        ('org_admin', 'Organization Admin'),
        ('ops_user', 'Operations User'),
        ('broker_user', 'Broker User'),
        ('member_user', 'Member User'),
    ]

    email = models.EmailField(unique=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    role = models.CharField(max_length=30, choices=ROLE_TYPES, default='member_user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
