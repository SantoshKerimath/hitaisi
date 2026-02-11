# Architecture Overview

## Modular Apps

identity/
benefits/
tickets/
audit/
claims/

## Service Layer

benefits/services/premium_engine.py

## Authentication

JWT via SimpleJWT

## Event Tracking

Django signals -> AuditEvent

## CI/CD

GitHub Actions
pytest
pytest-html

## Future Scalability

- PostgreSQL
- Dockerized deployment
- Horizontal scaling
- Role-based permissions engine
