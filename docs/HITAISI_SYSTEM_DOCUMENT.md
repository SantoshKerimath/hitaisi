---
# 🏥 HITAISI


**Health Insurance Benefits Technology Infrastructure Platform**

Version: 1.0 (Architecture Freeze – Prototype Complete)
---
# 1️⃣ Executive Summary

HITAISI is a modular, API-first health insurance administration backend designed to manage:

* Organizations (Insurer / Employer / Broker)
* Policies
* Members & Dependents
* Premium Calculations
* Claims
* Support Tickets
* Audit Logs

The system is built using Django REST Framework and follows a scalable modular architecture to support future SaaS deployment.

This document defines:

* Current system state
* Architectural decisions
* Testing & CI process
* Deployment plan
* Future roadmap

---

# 2️⃣ Current System State (Prototype Complete)

## ✅ Authentication & Identity

* JWT Authentication using SimpleJWT
* Organization-based user mapping
* Role-based user classification
* API Versioning: `/api/v1/`
* OpenAPI documentation via drf-spectacular

---

## ✅ Core Apps

### identity/

* Organization
* User (custom user model)
* Role handling

### benefits/

* Client
* Product
* Policy
* Member
* PremiumRate
* PremiumBuffer
* Policy documents
* Premium engine service

### claims/

* Claim
* Claim status lifecycle

### tickets/

* SupportTicket
* TicketMessage
* Modular assignment system
* Status workflow (open → in_progress → closed)

### audit/

* AuditEvent model
* Automatic CRUD capture via signals

---

# 3️⃣ Premium Engine (Business Logic Layer)

Premium calculation is centralized in:

<pre class="overflow-visible! px-0!" data-start="1615" data-end="1658"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>benefits/services/premium_engine.py
</span></span></code></div></div></pre>

Premium calculation based on:

* Product
* Relation
* Age band
* Sum insured

Triggers:

* Member creation
* Dependent addition
* Member deletion

Updates:

* PremiumBuffer.premium_used

All validated by automated tests.

---

# 4️⃣ API Structure

Base path:

<pre class="overflow-visible! px-0!" data-start="1920" data-end="1936"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>/api/v1/
</span></span></code></div></div></pre>

Main endpoints:

<pre class="overflow-visible! px-0!" data-start="1955" data-end="2184"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>/api/</span><span>v1</span><span>/auth/</span><span>login</span><span>/</span><span>
</span><span>/api/</span><span>v1</span><span>/clients/</span><span>
</span><span>/api/</span><span>v1</span><span>/products/</span><span>
</span><span>/api/</span><span>v1</span><span>/policies/</span><span>
</span><span>/api/</span><span>v1</span><span>/members/</span><span>
</span><span>/api/</span><span>v1</span><span>/member/</span><span>dependents</span><span>/add/</span><span>
</span><span>/api/</span><span>v1</span><span>/tickets/</span><span>create</span><span>/</span><span>
</span><span>/api/</span><span>v1</span><span>/claims/</span><span>
</span><span>/api/</span><span>v1</span><span>/audit/</span><span>
</span><span>/api/</span><span>v1</span><span>/health/</span><span>
</span><span>/api/</span><span>v1</span><span>/docs/</span><span>
</span><span>/api/</span><span>v1</span><span>/schema/</span><span>
</span></span></code></div></div></pre>

---

# 5️⃣ Architecture Overview

### System Flow

Client → DRF View → Service Layer → ORM → Database

### Architectural Principles

1. API-first backend
2. Modular apps
3. Business logic in services
4. Signals only for audit/logging
5. Test-first validation
6. Versioned API
7. CI enforced

---

# 6️⃣ Testing & CI

Framework:

* pytest
* pytest-django
* DRF APIClient

Coverage:

* Identity login
* Member lifecycle
* Policy flow
* Premium engine
* Ticket creation
* Audit logging

CI:

* GitHub Actions
* Runs on push
* Generates coverage report

Rule:

> No merge without passing tests.

---

# 7️⃣ Documentation System

* Swagger UI via drf-spectacular
* OpenAPI schema generation
* Living system document (this file)

---

# 8️⃣ Known Constraints

* SQLite used in development
* PostgreSQL required for production
* Role system currently static (to be modularized later)
* Ticket workflow simple (workflow engine planned)

---

# 9️⃣ Architecture Freeze (v1)

The following decisions are frozen:

* Django REST Framework
* JWT Authentication
* Modular app structure
* Versioned API
* Service-layer premium engine
* Audit via signals
* GitHub CI pipeline

Focus now shifts from feature building → production readiness.

---

# 🔟 Immediate Next Actions (Deployment Phase)

## Step 1 – Production Database

Switch from SQLite → PostgreSQL

Tasks:

* Install psycopg2
* Create production database config
* Environment-based DB switching

---

## Step 2 – Dockerization

Create:

* Dockerfile
* docker-compose.yml
* .env file

Containers:

* Django
* PostgreSQL

---

## Step 3 – Production Settings

Create:

<pre class="overflow-visible! px-0!" data-start="3791" data-end="3862"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>core/settings/
    base.py
    development.py
    production.py
</span></span></code></div></div></pre>

Set:

* DEBUG=False
* Secure cookies
* CORS config
* ALLOWED_HOSTS
* Logging config

---

## Step 4 – Deployment

Option A (Fastest):

* Render

Option B (Professional):

* DigitalOcean VPS
* Nginx
* Gunicorn
* PostgreSQL

---

# 1️⃣1️⃣ Future Roadmap

## Phase 2 – Permission Engine

Dynamic role-permission mapping.

## Phase 3 – Ticket Workflow Engine

Escalation rules, SLA tracking.

## Phase 4 – Claims Workflow

Approval pipeline, reserve logic.

## Phase 5 – Observability

Logging, monitoring, error tracking.

## Phase 6 – SaaS Readiness

Multi-tenant billing system.

---

# 1️⃣2️⃣ Engineering Standards

* Every feature must have tests
* Business logic must not live in views
* No silent failures
* No direct DB mutations in tests bypassing logic
* CI must stay green

---

# 1️⃣3️⃣ System Status

✅ Working prototype

✅ Automated tests passing

✅ CI enabled

✅ API documented

✅ Architecture frozen

Next phase: Production Deployment

---

# END OF DOCUMENT

Version 1.0

Architecture Freeze Date: 18 February 2026

---
