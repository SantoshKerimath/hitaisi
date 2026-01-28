from django.db import models
from benefits.models import Policy, Member

class Claim(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    claim_number = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="registered")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.claim_number
