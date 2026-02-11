from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import connection
from audit.models import AuditEvent
from audit.middleware import get_current_user


def audit_table_exists():
    """
    Prevent audit from running before audit tables are created
    (important during migrations and test DB setup).
    """
    return "audit_auditevent" in connection.introspection.table_names()


def should_skip(sender):
    """
    Skip:
    - AuditEvent itself (avoid recursion)
    - Django migration recorder
    """
    return (
        sender.__name__ == "AuditEvent"
        or sender._meta.app_label in ["contenttypes", "auth", "admin", "sessions"]
    )


@receiver(post_save)
def audit_save(sender, instance, created, **kwargs):
    if not audit_table_exists():
        return

    if should_skip(sender):
        return

    user = get_current_user()

    try:
        AuditEvent.objects.create(
            user=user if user and user.is_authenticated else None,
            action="CREATE" if created else "UPDATE",
            table=sender.__name__,
            record_id=instance.pk,
        )
    except Exception:
        pass


@receiver(post_delete)
def audit_delete(sender, instance, **kwargs):
    if not audit_table_exists():
        return

    if should_skip(sender):
        return

    user = get_current_user()

    try:
        AuditEvent.objects.create(
            user=user if user and user.is_authenticated else None,
            action="DELETE",
            table=sender.__name__,
            record_id=instance.pk,
        )
    except Exception:
        pass