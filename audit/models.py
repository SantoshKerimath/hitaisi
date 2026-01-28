from django.db import models
from identity.models import User

class AuditEvent(models.Model):
    ACTIONS = [
        ('CREATE', 'CREATE'),
        ('UPDATE', 'UPDATE'),
        ('DELETE', 'DELETE')
    ]

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=10, choices=ACTIONS)
    table = models.CharField(max_length=100)
    record_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} {self.table}({self.record_id})"
