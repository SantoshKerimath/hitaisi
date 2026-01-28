from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from audit.models import AuditEvent
from audit.middleware import get_current_user

@receiver(post_save)
def audit_save(sender, instance, created, **kwargs):
    # Skip audit app itself to avoid recursion
    if sender.__name__ == "AuditEvent":
        return

    user = get_current_user()

    AuditEvent.objects.create(
        user=user if user and user.is_authenticated else None,
        action="CREATE" if created else "UPDATE",
        table=sender.__name__,
        record_id=instance.id
    )

@receiver(post_delete)
def audit_delete(sender, instance, **kwargs):
    if sender.__name__ == "AuditEvent":
        return

    user = get_current_user()

    AuditEvent.objects.create(
        user=user if user and user.is_authenticated else None,
        action="DELETE",
        table=sender.__name__,
        record_id=instance.id
    )
