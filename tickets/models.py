from django.db import models
from identity.models import User
from benefits.models import Policy

class SupportTicket(models.Model):
    STATUS = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name="tickets")
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets_raised")
    assigned_to_role = models.CharField(max_length=30)  # ops_user / broker_user / org_admin
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} ({self.status})"

class TicketMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg by {self.sender.email} at {self.created_at}"

