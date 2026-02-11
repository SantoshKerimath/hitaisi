# HITAISI – Test Scenarios

## TS-01: Platform Admin Login

Objective: Validate JWT authentication
Steps:

1. Create org
2. Create admin user
3. Login via /api/auth/login/
   Expected:

- 200 OK
- Access token returned

---

## TS-02: HR Adds Employee

Objective: Ensure premium calculation and buffer update

Steps:

1. Create employer org
2. Create HR user
3. Create product
4. Configure premium rate
5. Create issued policy
6. HR logs in
7. HR adds employee member

Expected:

- 201 Created
- Premium assigned correctly
- PremiumBuffer updated

---

## TS-03: Premium Engine

Objective: Validate demographic-based pricing

Expected:

- Correct premium fetched from PremiumRate
- Error thrown if no rate configured

---

## TS-04: Dependent Add/Delete

Expected:

- Premium recalculated
- Ledger updated
