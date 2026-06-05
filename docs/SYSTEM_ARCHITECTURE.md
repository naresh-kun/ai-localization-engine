# System Architecture

## AI-Powered Multilingual Content Localization Engine

---

## Table of Contents

1. [High-Level Architecture](#1-high-level-architecture)
2. [FastAPI Architecture](#2-fastapi-architecture)
3. [Service Layer Design](#3-service-layer-design)
4. [Repository Layer Design](#4-repository-layer-design)
5. [Localization Workflow](#5-localization-workflow)
6. [Authentication Workflow](#6-authentication-workflow)
7. [Request Lifecycle](#7-request-lifecycle)

---

## 1. High-Level Architecture

### System Overview

The system follows a **layered clean architecture** with strict separation of concerns. Each layer has a single responsibility and communicates only with its adjacent layers through well-defined interfaces.

```
┌─────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                        │
│               React + TypeScript SPA                    │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP / REST
┌──────────────────────▼──────────────────────────────────┐
│                    API GATEWAY                          │
│              FastAPI Application Server                 │
│  ┌───────────────────────────────────────────────────┐  │
│  │                  API Layer                        │  │
│  │         (Routers / Endpoints / Schemas)           │  │
│  ├───────────────────────────────────────────────────┤  │
│  │                Service Layer                      │  │
│  │          (Business Logic / Orchestration)         │  │
│  ├───────────────────────────────────────────────────┤  │
│  │              Repository Layer                     │  │
│  │         (Data Access / Query Abstraction)         │  │
│  ├───────────────────────────────────────────────────┤  │
│  │               Database Layer                      │  │
│  │         (SQLAlchemy ORM / Models / Migrations)    │  │
│  └───────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │PostgreSQL│  │ AI / NLP │  │  External │
   │ Database │  │ Services │  │  APIs     │
   └──────────┘  └──────────┘  └──────────┘
```

### Layer Responsibilities

| Layer | Responsibility | Communicates With |
|---|---|---|
| **Client** | UI rendering, user interaction, API consumption | API Layer |
| **API Layer** | Request validation, routing, response serialization | Service Layer |
| **Service Layer** | Business logic, orchestration, domain rules | Repository Layer, External Services |
| **Repository Layer** | Data access abstraction, query building | Database Layer |
| **Database Layer** | ORM models, migrations, connection management | PostgreSQL |

### Architectural Principles

* **Dependency Inversion** — Upper layers depend on abstractions, not concrete implementations.
* **Single Responsibility** — Each module, class, and function has one reason to change.
* **Interface Segregation** — Consumers depend only on the interfaces they use.
* **Separation of Concerns** — Business logic never leaks into routers; data access never leaks into services.

### Project Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application factory
│   ├── config.py                  # Settings and environment configuration
│   ├── dependencies.py            # Dependency injection definitions
│   │
│   ├── api/                       # API Layer
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py          # Aggregated v1 router
│   │   │   ├── auth.py            # Authentication endpoints
│   │   │   ├── users.py           # User management endpoints
│   │   │   ├── projects.py        # Project endpoints
│   │   │   ├── localization.py    # Localization endpoints
│   │   │   ├── versions.py        # Version control endpoints
│   │   │   └── analytics.py       # Analytics endpoints
│   │   └── deps.py                # Route-level dependencies
│   │
│   ├── schemas/                   # Pydantic request/response models
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── localization.py
│   │   ├── version.py
│   │   └── analytics.py
│   │
│   ├── services/                  # Service Layer
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── project_service.py
│   │   ├── localization_service.py
│   │   ├── version_service.py
│   │   └── analytics_service.py
│   │
│   ├── repositories/              # Repository Layer
│   │   ├── __init__.py
│   │   ├── base.py                # Abstract base repository
│   │   ├── user_repository.py
│   │   ├── project_repository.py
│   │   ├── localization_repository.py
│   │   └── version_repository.py
│   │
│   ├── models/                    # Database Layer (SQLAlchemy ORM)
│   │   ├── __init__.py
│   │   ├── base.py                # Declarative base, common mixins
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── content.py
│   │   ├── translation.py
│   │   └── version.py
│   │
│   ├── core/                      # Cross-cutting concerns
│   │   ├── __init__.py
│   │   ├── security.py            # JWT, hashing, token utilities
│   │   ├── exceptions.py          # Custom exception classes
│   │   ├── logging.py             # Logging configuration
│   │   └── middleware.py          # CORS, error handling middleware
│   │
│   └── localization/              # AI/NLP engine
│       ├── __init__.py
│       ├── detector.py            # Language detection
│       ├── translator.py          # Translation engine
│       ├── adapter.py             # Cultural adaptation
│       └── scorer.py              # Quality scoring
│
├── alembic/                       # Database migrations
│   ├── versions/
│   └── env.py
├── alembic.ini
├── requirements.txt
├── Dockerfile
└── .env.example
```

---

## 2. FastAPI Architecture

### Application Factory

The application is created through a factory function in `main.py`. This pattern allows multiple configurations (testing, development, production) without code duplication.

```
main.py
  │
  ├── create_app()
  │     ├── Initialize FastAPI instance
  │     ├── Load configuration from environment
  │     ├── Register middleware (CORS, error handling, logging)
  │     ├── Register startup/shutdown events (DB pool)
  │     ├── Include API routers (v1)
  │     └── Return configured app
  │
  └── Uvicorn entry point
```

### Router Organization

Routers are organized by domain and versioned under `/api/v1/`. Each router file corresponds to a single domain module.

```
/api/v1/
  ├── /auth          →  auth.py       (login, register, refresh)
  ├── /users         →  users.py      (profile, list, admin ops)
  ├── /projects      →  projects.py   (CRUD, membership)
  ├── /localization  →  localization.py (submit, status, results)
  ├── /versions      →  versions.py   (save, restore, compare)
  └── /analytics     →  analytics.py  (stats, quality metrics)
```

### Dependency Injection

FastAPI's `Depends()` mechanism is used throughout to inject:

| Dependency | Purpose | Scope |
|---|---|---|
| `get_db` | Yields a SQLAlchemy session per request | Request |
| `get_current_user` | Extracts and validates JWT from headers | Request |
| `get_current_admin` | Validates JWT + admin role | Request |
| `get_*_service` | Constructs service with injected repository | Request |
| `get_*_repository` | Constructs repository with injected session | Request |

**Injection chain:**

```
Router Endpoint
  └── Depends(get_localization_service)
        └── Depends(get_localization_repository)
              └── Depends(get_db)
                    └── SessionLocal (from connection pool)
```

### Pydantic Schemas

Schemas enforce strict validation at the API boundary. Each domain has a family of schemas:

```
schemas/project.py
  ├── ProjectCreate        (input: create)
  ├── ProjectUpdate        (input: partial update)
  ├── ProjectResponse      (output: single resource)
  ├── ProjectListResponse  (output: paginated list)
  └── ProjectFilter        (input: query parameters)
```

**Design rules:**

* Request schemas never expose internal fields (`id`, `created_at`).
* Response schemas always include `id` and timestamps.
* All schemas inherit from a `BaseSchema` with `model_config` for ORM mode.

### Error Handling

A global exception handler middleware catches all exceptions and maps them to consistent JSON responses:

```
Exception Hierarchy
  ├── AppException (base)
  │   ├── NotFoundException       → 404
  │   ├── UnauthorizedException   → 401
  │   ├── ForbiddenException      → 403
  │   ├── ValidationException     → 422
  │   ├── ConflictException       → 409
  │   └── InternalException       → 500
  │
  └── Unhandled Exception         → 500 (logged, generic message returned)
```

**Standard error response body:**

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Project with id '...' not found.",
    "details": null
  }
}
```

---

## 3. Service Layer Design

### Purpose

The service layer is the **sole owner of business logic**. It orchestrates operations across repositories, enforces domain rules, and coordinates with external services (AI/NLP engines).

### Design Principles

* **No direct database access** — Services call repositories, never SQLAlchemy sessions.
* **No HTTP concerns** — Services never read headers, return HTTP status codes, or raise HTTP exceptions.
* **Transaction boundaries** — Services define the unit-of-work boundary; a single service method call equals one transaction.
* **Domain exceptions** — Services raise domain-specific exceptions (e.g., `ProjectNotFoundException`), which the API layer maps to HTTP responses.

### Service Structure

Each service follows a consistent internal structure:

```
class ProjectService:
    │
    ├── __init__(repository: ProjectRepository)
    │
    ├── create_project(data, current_user)
    │     ├── Validate business rules
    │     ├── Call repository.create()
    │     └── Return created entity
    │
    ├── get_project(project_id, current_user)
    │     ├── Call repository.get_by_id()
    │     ├── Check ownership / membership
    │     └── Return entity or raise NotFoundException
    │
    ├── update_project(project_id, data, current_user)
    │     ├── Fetch existing entity
    │     ├── Validate ownership
    │     ├── Apply updates
    │     └── Call repository.update()
    │
    ├── delete_project(project_id, current_user)
    │     ├── Validate ownership
    │     ├── Call repository.delete()
    │     └── Cascade cleanup (versions, translations)
    │
    └── list_projects(filters, current_user)
          ├── Apply ownership filter
          ├── Call repository.list()
          └── Return paginated results
```

### Service Interaction Map

Services collaborate when operations span multiple domains:

```
LocalizationService
  ├── uses → ProjectRepository      (verify project ownership)
  ├── uses → LocalizationRepository (persist translation results)
  ├── uses → VersionRepository      (auto-save version on completion)
  ├── calls → detector.detect()     (language detection)
  ├── calls → translator.translate() (translation)
  ├── calls → adapter.adapt()       (cultural adaptation)
  └── calls → scorer.score()        (quality scoring)
```

```
AnalyticsService
  ├── uses → LocalizationRepository (aggregation queries)
  ├── uses → ProjectRepository      (project-scoped stats)
  └── uses → UserRepository         (user activity metrics)
```

### Cross-Cutting Concerns in Services

| Concern | Implementation |
|---|---|
| **Logging** | Structured logging at method entry/exit and on errors via Python `logging` module |
| **Validation** | Domain rule validation (beyond schema validation) within service methods |
| **Authorization** | Ownership and role checks performed in service methods before data mutation |
| **Idempotency** | Duplicate submission detection for localization requests |

---

## 4. Repository Layer Design

### Purpose

The repository layer provides a **clean abstraction over data access**. It encapsulates all SQLAlchemy query logic, preventing ORM details from leaking into the service layer.

### Base Repository

All repositories inherit from an abstract base that provides standard CRUD operations:

```
BaseRepository[T]
  │
  ├── get_by_id(id: UUID) → T | None
  ├── get_all(skip: int, limit: int) → list[T]
  ├── create(entity: T) → T
  ├── update(entity: T) → T
  ├── delete(id: UUID) → None
  └── count() → int
```

**Generic type `T`** is bound to the SQLAlchemy model class, ensuring type safety across the repository hierarchy.

### Specialized Repositories

Each domain repository extends the base with domain-specific query methods:

```
UserRepository(BaseRepository[User])
  ├── get_by_email(email: str) → User | None
  └── get_by_role(role: str) → list[User]

ProjectRepository(BaseRepository[Project])
  ├── get_by_owner(user_id: UUID) → list[Project]
  ├── get_with_stats(project_id: UUID) → ProjectWithStats
  └── search(query: str, user_id: UUID) → list[Project]

LocalizationRepository(BaseRepository[Translation])
  ├── get_by_project(project_id: UUID) → list[Translation]
  ├── get_by_language_pair(source: str, target: str) → list[Translation]
  ├── get_latest_by_content(content_id: UUID) → Translation | None
  └── aggregate_quality_scores(project_id: UUID) → QualityStats

VersionRepository(BaseRepository[Version])
  ├── get_by_translation(translation_id: UUID) → list[Version]
  ├── get_latest_version(translation_id: UUID) → Version | None
  └── compare_versions(v1_id: UUID, v2_id: UUID) → VersionDiff
```

### Session Management

```
Request arrives
  │
  ├── Dependency `get_db()` yields a new session from the connection pool
  ├── Session is injected into repository constructor
  ├── Repository uses session for all queries within the request
  ├── On success: session.commit() is called by the service layer
  ├── On exception: session.rollback() is triggered automatically
  └── Finally: session.close() returns connection to pool
```

### Query Patterns

| Pattern | Use Case |
|---|---|
| **Eager loading** | `joinedload()` for related entities needed in the response (e.g., project with translations) |
| **Pagination** | All list queries accept `skip` and `limit` and return total count |
| **Filtering** | Filter objects are translated to SQLAlchemy `where` clauses in the repository |
| **Soft deletes** | Records are marked with `deleted_at` timestamp rather than removed |

---

## 5. Localization Workflow

### End-to-End Flow

```
User submits content
       │
       ▼
┌──────────────────┐
│  Content Receipt  │  API Layer receives text + target languages
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Language Detection│  Detect source language if not specified
│   (detector.py)  │  Output: ISO 639-1 language code + confidence
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Translation    │  Translate content to each target language
│ (translator.py)  │  Output: raw translated text per language
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│Cultural Adaptation│  Adapt tone, idioms, formatting per locale
│   (adapter.py)    │  Output: culturally adapted text per language
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Quality Scoring  │  Score each translation on multiple dimensions
│   (scorer.py)    │  Output: fluency, adequacy, cultural fit scores
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Persistence    │  Save translation + scores + version snapshot
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Response Return  │  Return results with quality metrics
└──────────────────┘
```

### Localization Pipeline Detail

**Stage 1 — Language Detection**

```
Input:  Raw text content
Process:
  ├── Run NLP-based language identification
  ├── Return detected language code (e.g., "en", "ta", "fr")
  └── Return confidence score (0.0 – 1.0)
Output: { language: "en", confidence: 0.97 }
```

**Stage 2 — Translation**

```
Input:  Source text + source language + list of target languages
Process:
  ├── For each target language:
  │     ├── Send to AI translation model
  │     ├── Preserve structural formatting (paragraphs, lists)
  │     └── Collect raw translation output
  └── Return map of language → translated text
Output: { "ta": "...", "fr": "...", "de": "..." }
```

**Stage 3 — Cultural Adaptation**

```
Input:  Raw translated text + target locale metadata
Process:
  ├── Adjust formality level per locale norms
  ├── Replace idioms with culturally equivalent expressions
  ├── Adapt date, number, and currency formatting conventions
  └── Adjust tone to match regional expectations
Output: Culturally adapted text per locale
```

**Stage 4 — Quality Scoring**

```
Input:  Source text + adapted translation
Process:
  ├── Fluency score     — grammatical correctness in target language
  ├── Adequacy score    — meaning preservation from source
  ├── Cultural fit score — appropriateness for target locale
  └── Overall score     — weighted composite
Output: { fluency: 0.92, adequacy: 0.88, cultural_fit: 0.85, overall: 0.88 }
```

### Version Control Integration

Every completed localization automatically creates a version snapshot:

```
Translation completed
  │
  ├── Version record created with:
  │     ├── version_number (auto-incremented per translation)
  │     ├── translated_content snapshot
  │     ├── quality_scores snapshot
  │     ├── source_content_hash (to detect source changes)
  │     └── created_at timestamp
  │
  └── Previous versions remain immutable and queryable
```

---

## 6. Authentication Workflow

### Technology

* **JWT (JSON Web Tokens)** for stateless authentication.
* **bcrypt** for password hashing.
* **Access + Refresh token** pattern for session management.

### Registration Flow

```
Client                         API              Service            Repository        Database
  │                             │                  │                    │                │
  │  POST /api/v1/auth/register │                  │                    │                │
  │  { email, password, name }  │                  │                    │                │
  │ ──────────────────────────► │                  │                    │                │
  │                             │  validate schema │                    │                │
  │                             │ ───────────────► │                    │                │
  │                             │                  │  check duplicate   │                │
  │                             │                  │ ─────────────────► │                │
  │                             │                  │                    │  SELECT by      │
  │                             │                  │                    │  email          │
  │                             │                  │                    │ ──────────────► │
  │                             │                  │                    │ ◄────────────── │
  │                             │                  │ ◄───────────────── │                │
  │                             │                  │                    │                │
  │                             │                  │  hash password     │                │
  │                             │                  │  (bcrypt)          │                │
  │                             │                  │                    │                │
  │                             │                  │  create user       │                │
  │                             │                  │ ─────────────────► │                │
  │                             │                  │                    │  INSERT         │
  │                             │                  │                    │ ──────────────► │
  │                             │                  │                    │ ◄────────────── │
  │                             │                  │ ◄───────────────── │                │
  │                             │                  │                    │                │
  │                             │                  │  generate tokens   │                │
  │                             │ ◄─────────────── │                    │                │
  │  { access_token,            │                  │                    │                │
  │    refresh_token }          │                  │                    │                │
  │ ◄────────────────────────── │                  │                    │                │
```

### Login Flow

```
Client                         API              Service            Repository        Database
  │                             │                  │                    │                │
  │  POST /api/v1/auth/login    │                  │                    │                │
  │  { email, password }        │                  │                    │                │
  │ ──────────────────────────► │                  │                    │                │
  │                             │  validate schema │                    │                │
  │                             │ ───────────────► │                    │                │
  │                             │                  │  find user         │                │
  │                             │                  │ ─────────────────► │                │
  │                             │                  │                    │  SELECT by      │
  │                             │                  │                    │  email          │
  │                             │                  │                    │ ──────────────► │
  │                             │                  │                    │ ◄────────────── │
  │                             │                  │ ◄───────────────── │                │
  │                             │                  │                    │                │
  │                             │                  │  verify password   │                │
  │                             │                  │  (bcrypt compare)  │                │
  │                             │                  │                    │                │
  │                             │                  │  generate tokens   │                │
  │                             │                  │  (access+refresh)  │                │
  │                             │ ◄─────────────── │                    │                │
  │  { access_token,            │                  │                    │                │
  │    refresh_token }          │                  │                    │                │
  │ ◄────────────────────────── │                  │                    │                │
```

### Token Structure

**Access Token (short-lived: 30 minutes)**

```json
{
  "sub": "<user_uuid>",
  "role": "user | admin",
  "exp": 1717634400,
  "iat": 1717632600,
  "type": "access"
}
```

**Refresh Token (long-lived: 7 days)**

```json
{
  "sub": "<user_uuid>",
  "exp": 1718237400,
  "iat": 1717632600,
  "type": "refresh"
}
```

### Token Refresh Flow

```
Client                         API              Service
  │                             │                  │
  │  POST /api/v1/auth/refresh  │                  │
  │  { refresh_token }          │                  │
  │ ──────────────────────────► │                  │
  │                             │ ───────────────► │
  │                             │                  │  Decode refresh token
  │                             │                  │  Validate expiry
  │                             │                  │  Verify user still exists + active
  │                             │                  │  Generate new access token
  │                             │                  │  Rotate refresh token
  │                             │ ◄─────────────── │
  │  { access_token,            │                  │
  │    refresh_token }          │                  │
  │ ◄────────────────────────── │                  │
```

### Protected Route Authorization

```
Request with Authorization header
  │
  ├── Middleware / Dependency extracts Bearer token
  ├── Decode JWT → validate signature + expiry
  ├── Extract user_id from "sub" claim
  ├── Load user from database (verify still active)
  ├── Attach user object to request state
  │
  ├── [If role required] Check user.role against required role
  │     ├── Match → proceed
  │     └── No match → 403 Forbidden
  │
  └── Proceed to endpoint handler
```

### Role-Based Access Control

```
                  ┌────────────────────┐
                  │    Public Routes   │
                  │  (no auth needed)  │
                  │  POST /auth/login  │
                  │  POST /auth/register│
                  └────────────────────┘

                  ┌────────────────────┐
                  │ Authenticated Routes│
                  │  (valid JWT needed) │
                  │  GET  /projects    │
                  │  POST /localization│
                  │  GET  /versions    │
                  └────────────────────┘

                  ┌────────────────────┐
                  │   Admin Routes     │
                  │ (JWT + admin role) │
                  │  GET  /users       │
                  │  GET  /analytics   │
                  │  DELETE /users/:id │
                  └────────────────────┘
```

---

## 7. Request Lifecycle

### Complete Request Journey

The following traces a localization request from client to database and back:

```
 ① CLIENT
    │
    │  POST /api/v1/localization/translate
    │  Headers: { Authorization: Bearer <jwt> }
    │  Body: { project_id, content, target_languages: ["ta","fr"] }
    │
    ▼
 ② MIDDLEWARE STACK
    │
    ├── CORS Middleware          → Validate origin, set headers
    ├── Logging Middleware       → Log request method, path, timestamp
    └── Error Handler Middleware → Wrap in try/catch for unhandled errors
    │
    ▼
 ③ DEPENDENCY RESOLUTION
    │
    ├── get_db()                → Create SQLAlchemy session from pool
    ├── get_current_user(token) → Decode JWT → Load user from DB
    ├── get_localization_repo(db) → Instantiate LocalizationRepository
    ├── get_project_repo(db)     → Instantiate ProjectRepository
    └── get_localization_service(repos) → Instantiate LocalizationService
    │
    ▼
 ④ ROUTER / ENDPOINT
    │
    ├── Pydantic validates request body against schema
    ├── Calls localization_service.translate(data, current_user)
    │
    ▼
 ⑤ SERVICE LAYER
    │
    ├── Verify project exists and user has access
    │     └── project_repo.get_by_id(project_id)
    │
    ├── Run localization pipeline:
    │     ├── detector.detect(content)
    │     ├── translator.translate(content, source_lang, target_langs)
    │     ├── adapter.adapt(translations, target_locales)
    │     └── scorer.score(source, translations)
    │
    ├── Persist results:
    │     ├── localization_repo.create(translation_records)
    │     └── version_repo.create(version_snapshots)
    │
    └── Return domain objects
    │
    ▼
 ⑥ REPOSITORY LAYER
    │
    ├── Build SQLAlchemy query objects
    ├── Execute against session
    ├── Map results to ORM model instances
    └── Return to service
    │
    ▼
 ⑦ DATABASE LAYER
    │
    ├── SQLAlchemy session executes SQL via connection pool
    ├── PostgreSQL processes queries
    ├── On success: session.commit()
    └── On failure: session.rollback()
    │
    ▼
 ⑧ RESPONSE SERIALIZATION
    │
    ├── Service returns domain objects to router
    ├── Router maps to Pydantic response schema
    ├── FastAPI serializes to JSON
    └── HTTP response with status code
    │
    ▼
 ⑨ MIDDLEWARE (outbound)
    │
    ├── Logging middleware logs response status + duration
    └── CORS headers attached
    │
    ▼
 ⑩ CLIENT receives response
    │
    └── { translations: [...], quality_scores: {...}, version_id: "..." }
```

### Error Path

When an error occurs at any layer, the flow short-circuits:

```
Error in Service Layer
  │
  ├── Service raises domain exception (e.g., ProjectNotFoundException)
  ├── Exception propagates to router
  ├── Router does NOT catch it
  ├── Error Handler Middleware intercepts
  │     ├── Maps exception class → HTTP status code
  │     ├── Formats standard error response body
  │     └── Logs error with request context
  ├── SQLAlchemy session is rolled back (via get_db() finally block)
  └── JSON error response returned to client
```

### Session & Connection Lifecycle

```
Connection Pool (startup)
  │
  │  Request arrives
  ├──────────────────────────►  Acquire connection from pool
  │                              │
  │                              ├── Create Session
  │                              ├── Bind to request scope
  │                              ├── Execute queries
  │                              │
  │  Request completes           │
  ├──────────────────────────►  ├── Commit or Rollback
  │                              ├── Close Session
  │                              └── Return connection to pool
  │
  │  Application shutdown
  └──────────────────────────►  Dispose all connections
```

---

## Summary

| Aspect | Decision |
|---|---|
| **Architecture style** | Layered clean architecture |
| **API framework** | FastAPI with versioned routers |
| **Validation** | Pydantic schemas at API boundary |
| **Business logic** | Service layer (no HTTP, no ORM leakage) |
| **Data access** | Repository pattern over SQLAlchemy |
| **Database** | PostgreSQL via SQLAlchemy ORM + Alembic migrations |
| **Authentication** | JWT (access + refresh tokens) |
| **Authorization** | Role-based (admin / user) via dependency injection |
| **Error handling** | Domain exceptions → middleware → standard JSON |
| **Logging** | Structured logging via middleware + service-level logging |
| **AI/NLP** | Modular pipeline: detect → translate → adapt → score |
| **Versioning** | Immutable version snapshots per translation |
