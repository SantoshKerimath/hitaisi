from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date

from identity.models import Organization, User
from benefits.models import (
    Client, Product, ProductCoverage,
    Policy, Member, PremiumBuffer
)

class Command(BaseCommand):
    help = "Bootstrap full test data for HITAISI platform"

    def handle(self, *args, **options):
        self.stdout.write("🚀 Bootstrapping HITAISI test data...")

        # ---------- Organizations ----------
        platform_org, _ = Organization.objects.get_or_create(
            name="HITAISI Platform",
            org_type="platform"
        )

        employer_org, _ = Organization.objects.get_or_create(
            name="Acme Employer",
            org_type="employer"
        )

        # ---------- Users ----------
        platform_admin, _ = User.objects.get_or_create(
            email="admin@hitaisi.com",
            defaults={
                "username": "platform_admin",
                "role": "platform_admin",
                "organization": platform_org,
                "is_staff": True,
                "is_superuser": True
            }
        )
        platform_admin.set_password("Admin@123")
        platform_admin.save()

        hr_admin, _ = User.objects.get_or_create(
            email="hr@acme.com",
            defaults={
                "username": "hr_admin",
                "role": "org_admin",
                "organization": employer_org
            }
        )
        hr_admin.set_password("Hr@123")
        hr_admin.save()

        # ---------- Client ----------
        client, _ = Client.objects.get_or_create(
            name="Acme Corp Client",
            organization=employer_org
        )

        # ---------- Product ----------
        product, _ = Product.objects.get_or_create(
            name="Standard Group Health",
            base_sum_insured=500000
        )

        ProductCoverage.objects.get_or_create(
            product=product,
            coverage_name="Hospitalization",
            defaults={"is_covered": True}
        )

        ProductCoverage.objects.get_or_create(
            product=product,
            coverage_name="Maternity",
            defaults={
                "is_covered": True,
                "has_sublimit": True,
                "sublimit_amount": 50000
            }
        )

        # ---------- Policy ----------
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=365)

        policy, _ = Policy.objects.get_or_create(
            policy_number="POL-TEST-001",
            client=client,
            product=product,
            defaults={
                "status": "issued",
                "start_date": start_date,
                "end_date": end_date
            }
        )

        # ---------- Premium Buffer ----------
        buffer, _ = PremiumBuffer.objects.get_or_create(policy=policy)


        today = date.today()
        employee_dob = date(today.year - 30, today.month, today.day)
        spouse_dob = date(today.year - 28, today.month, today.day)

        # ---------- Members ----------
        employee, _ = Member.objects.get_or_create(
            policy=policy,
            employee_code="EMP001",
            relation="employee",
            defaults={
                "name": "John Employee",
                "date_of_birth": employee_dob,
                "age": 30,
                "gender": "male",
                "sum_insured": 500000,
                "cover_start_date": start_date,
                "cover_end_date": end_date,
            }
        )
        spouse, _ = Member.objects.get_or_create(
            policy=policy,
            employee_code="EMP001",
            relation="spouse",
            defaults={
                "name": "Jane Spouse",
                "date_of_birth": spouse_dob,
                "age": 28,
                "gender": "female",
                "sum_insured": 300000,
                "cover_start_date": start_date,
                "cover_end_date": end_date,
            }
        )


        buffer.recalc()

        self.stdout.write(self.style.SUCCESS("✅ Bootstrap completed successfully"))
        self.stdout.write("🔑 Platform Admin: admin@hitaisi.com / Admin@123")
        self.stdout.write("🔑 HR Admin: hr@acme.com / Hr@123")
