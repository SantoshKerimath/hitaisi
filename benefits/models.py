from django.db import models
from identity.models import Organization, User


class Client(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    base_sum_insured = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductCoverage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="coverages")
    coverage_name = models.CharField(max_length=255)
    is_covered = models.BooleanField(default=True)
    has_sublimit = models.BooleanField(default=False)
    sublimit_amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.coverage_name}"


class Policy(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('in_force', 'In Force'),
    ]

    policy_number = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="policies")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.policy_number


class PolicyCoverage(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name="policy_coverages")
    coverage_name = models.CharField(max_length=255)
    is_covered = models.BooleanField(default=True)
    sublimit_amount = models.IntegerField(null=True, blank=True)



class Member(models.Model):
    RELATION_CHOICES = [
        ('employee', 'Employee'),
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('parent', 'Parent'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name="members")
    name = models.CharField(max_length=255)
    relation = models.CharField(max_length=20, choices=RELATION_CHOICES)
    employee_code = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.IntegerField()
    sum_insured = models.IntegerField()
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    cover_start_date = models.DateField()
    cover_end_date = models.DateField()
    premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} ({self.relation})"


class PolicyDocument(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="policy_docs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PremiumBuffer(models.Model):
    policy = models.OneToOneField(Policy, on_delete=models.CASCADE, related_name="premium_buffer")
    total_premium_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    premium_used = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def recalc(self):
        self.outstanding_balance = self.total_premium_paid - self.premium_used
        self.save()


class PremiumRate(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    relation = models.CharField(max_length=50)  # employee / spouse / child / parent
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    sum_insured = models.IntegerField()
    annual_premium = models.DecimalField(max_digits=10, decimal_places=2)
