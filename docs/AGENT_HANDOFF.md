# Agent Handoff Document

## Backend Completion Checklist

* [ ] Database schema completed
* [ ] API endpoints completed
* [ ] Authentication completed
* [ ] Localization engine completed
* [ ] Docker configuration completed
* [ ] Unit tests completed
* [ ] Integration tests completed
* [ ] API documentation completed

---

## Frontend Start Checklist

Before starting frontend development:

* Read PROJECT_OVERVIEW.md
* Read SYSTEM_ARCHITECTURE.md
* Read DATABASE_DESIGN.md
* Read API_SPECIFICATION.md

---

## API Contract Rules

Frontend must never assume API structures.

Always use:

API_SPECIFICATION.md

as the single source of truth.

---

## Communication Rules

If backend changes:

Update:

* API_SPECIFICATION.md
* DATABASE_DESIGN.md

before merging.

If frontend requires changes:

Create:
CHANGE_REQUEST.md

and submit request before modification.
