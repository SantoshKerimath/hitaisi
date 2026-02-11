# HITAISI – Functional Test Cases

## TC-01: Platform Bootstrap

- Run: python manage.py bootstrap_test_data
- Expected:
  - Platform admin exists
  - Employer org exists
  - Policy in ISSUED state
  - Members created

## TC-02: HR Login

- API: POST /api/auth/login/
- Role: org_admin
- Expected: JWT token returned

## TC-03: Member Addition

- API: POST /api/member/dependents/add/
- Expected:
  - Premium recalculated
  - Audit event created

## TC-04: Ticket Conversation

- API: POST /api/tickets/create/
- API: POST /api/tickets/message/add/
- Expected:
  - Ticket status updated
  - Messages threaded
