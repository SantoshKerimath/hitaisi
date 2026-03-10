import pytest
from identity.models import Organization

@pytest.mark.django_db
def test_audit_event_triggered():
    org = Organization.objects.create(
        name="Audit Test Org",
        org_type="employer"
    )

    from audit.models import AuditEvent
    assert AuditEvent.objects.count() > 0
