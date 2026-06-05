# Backend Folder Structure

## AI-Powered Multilingual Content Localization Engine

---

## Complete Folder Tree

```
backend/
│
├── app/                                    # Application root package
│   ├── __init__.py                         # Package initializer
│   ├── main.py                             # FastAPI application factory and entry point
│   ├── config.py                           # Settings and environment variable configuration
│   │
│   ├── api/                                # API Layer — HTTP interface
│   │   ├── __init__.py
│   │   ├── deps.py                         # Shared route-level dependencies
│   │   └── v1/                             # Version 1 API routes
│   │       ├── __init__.py
│   │       ├── router.py                   # Aggregated v1 router (includes all sub-routers)
│   │       ├── auth.py                     # Authentication endpoints (register, login, refresh, logout)
│   │       ├── users.py                    # User management endpoints (profile, admin operations)
│   │       ├── projects.py                 # Project CRUD endpoints
│   │       ├── contents.py                 # Content submission and retrieval endpoints
│   │       ├── localization.py             # Localization pipeline endpoints
│   │       ├── translations.py             # Translation retrieval and version endpoints
│   │       └── analytics.py               # Analytics and dashboard endpoints
│   │
│   ├── schemas/                            # Pydantic request/response models
│   │   ├── __init__.py
│   │   ├── base.py                         # Base schema with shared configuration
│   │   ├── auth.py                         # Auth schemas (LoginRequest, RegisterRequest, TokenResponse)
│   │   ├── user.py                         # User schemas (UserResponse, UserUpdate)
│   │   ├── project.py                      # Project schemas (ProjectCreate, ProjectUpdate, ProjectResponse)
│   │   ├── content.py                      # Content schemas (ContentCreate, ContentResponse)
│   │   ├── localization.py                 # Localization schemas (LocalizeRequest, LocalizeResponse)
│   │   ├── translation.py                 # Translation schemas (TranslationResponse, VersionResponse)
│   │   ├── analytics.py                   # Analytics schemas (DashboardResponse, LanguageUsage)
│   │   └── common.py                       # Shared schemas (PaginatedResponse, ErrorResponse)
│   │
│   ├── services/                           # Service Layer — Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py                 # Authentication and token management logic
│   │   ├── user_service.py                 # User account management logic
│   │   ├── project_service.py              # Project lifecycle management logic
│   │   ├── content_service.py              # Content submission and retrieval logic
│   │   ├── localization_service.py         # Localization pipeline orchestration
│   │   ├── translation_service.py          # Translation retrieval and version management
│   │   └── analytics_service.py            # Analytics aggregation and statistics logic
│   │
│   ├── repositories/                       # Repository Layer — Data access abstraction
│   │   ├── __init__.py
│   │   ├── base.py                         # Abstract generic base repository (CRUD operations)
│   │   ├── user_repository.py              # User-specific data access queries
│   │   ├── project_repository.py           # Project-specific data access queries
│   │   ├── content_repository.py           # Content-specific data access queries
│   │   ├── translation_repository.py       # Translation-specific data access queries
│   │   ├── version_repository.py           # Version snapshot data access queries
│   │   ├── quality_score_repository.py     # Quality score data access queries
│   │   ├── language_repository.py          # Supported languages data access queries
│   │   └── refresh_token_repository.py     # Refresh token data access queries
│   │
│   ├── models/                             # Database Layer — SQLAlchemy ORM models
│   │   ├── __init__.py                     # Model registry (imports all models for Alembic discovery)
│   │   ├── base.py                         # Declarative base, common mixins (timestamps, soft delete)
│   │   ├── user.py                         # User model
│   │   ├── project.py                      # Project model
│   │   ├── content.py                      # Content model
│   │   ├── translation.py                  # Translation model
│   │   ├── quality_score.py                # Quality score model
│   │   ├── translation_version.py          # Translation version snapshot model
│   │   ├── supported_language.py           # Supported language reference model
│   │   ├── refresh_token.py                # Refresh token model
│   │   └── audit_log.py                    # Audit log model
│   │
│   ├── database/                           # Database configuration and session management
│   │   ├── __init__.py
│   │   ├── session.py                      # SQLAlchemy engine, session factory, connection pool
│   │   └── seed.py                         # Initial seed data (supported languages, admin user)
│   │
│   ├── core/                               # Cross-cutting concerns
│   │   ├── __init__.py
│   │   ├── security.py                     # JWT encode/decode, password hashing, token utilities
│   │   ├── exceptions.py                   # Custom exception hierarchy (domain exceptions)
│   │   ├── logging.py                      # Structured logging configuration
│   │   └── middleware.py                   # CORS, request logging, global error handling middleware
│   │
│   └── localization/                       # AI/NLP localization engine
│       ├── __init__.py
│       ├── detector.py                     # Language detection module
│       ├── translator.py                   # Translation engine module
│       ├── adapter.py                      # Cultural adaptation module
│       └── scorer.py                       # Quality scoring module
│
├── alembic/                                # Database migrations (Alembic)
│   ├── versions/                           # Migration version scripts
│   │   └── .gitkeep
│   ├── env.py                              # Alembic environment configuration
│   └── script.py.mako                      # Migration script template
│
├── tests/                                  # Test suite
│   ├── __init__.py
│   ├── conftest.py                         # Shared pytest fixtures (test DB, client, auth helpers)
│   │
│   ├── unit/                               # Unit tests (isolated, no DB)
│   │   ├── __init__.py
│   │   ├── services/                       # Service layer unit tests
│   │   │   ├── __init__.py
│   │   │   ├── test_auth_service.py
│   │   │   ├── test_user_service.py
│   │   │   ├── test_project_service.py
│   │   │   ├── test_content_service.py
│   │   │   ├── test_localization_service.py
│   │   │   ├── test_translation_service.py
│   │   │   └── test_analytics_service.py
│   │   ├── repositories/                   # Repository layer unit tests
│   │   │   ├── __init__.py
│   │   │   ├── test_user_repository.py
│   │   │   ├── test_project_repository.py
│   │   │   ├── test_content_repository.py
│   │   │   ├── test_translation_repository.py
│   │   │   └── test_version_repository.py
│   │   └── localization/                   # Localization engine unit tests
│   │       ├── __init__.py
│   │       ├── test_detector.py
│   │       ├── test_translator.py
│   │       ├── test_adapter.py
│   │       └── test_scorer.py
│   │
│   └── integration/                        # Integration tests (with DB and API)
│       ├── __init__.py
│       ├── test_auth_api.py                # Auth endpoint integration tests
│       ├── test_project_api.py             # Project endpoint integration tests
│       ├── test_content_api.py             # Content endpoint integration tests
│       ├── test_localization_api.py        # Localization endpoint integration tests
│       ├── test_translation_api.py         # Translation endpoint integration tests
│       └── test_analytics_api.py           # Analytics endpoint integration tests
│
├── alembic.ini                             # Alembic configuration file
├── requirements.txt                        # Python dependencies
├── Dockerfile                              # Container image definition
├── .env.example                            # Environment variable template
└── README.md                               # Backend developer documentation
```

---

## Folder Purpose Guide

### `app/` — Application Root

The main application package. Everything inside this folder is importable under the `app` namespace.

| File | Purpose |
|---|---|
| `main.py` | Application factory (`create_app()`). Initializes FastAPI, registers middleware, mounts routers, configures startup/shutdown events. Uvicorn entry point. |
| `config.py` | Loads all environment variables via Pydantic `BaseSettings`. Provides typed access to database URL, JWT secrets, CORS origins, and other configuration. |

---

### `app/api/` — API Layer

Handles HTTP concerns: routing, request parsing, response serialization. Contains zero business logic.

| File | Purpose |
|---|---|
| `deps.py` | Shared dependency functions used across all routers: `get_db()`, `get_current_user()`, `get_current_admin()`. |
| `v1/router.py` | Aggregates all v1 sub-routers into a single `APIRouter` with the `/api/v1` prefix. Mounted by `main.py`. |
| `v1/auth.py` | Routes for `/api/v1/auth/*` — register, login, refresh, logout. |
| `v1/users.py` | Routes for `/api/v1/users/*` — user profile, admin user management. |
| `v1/projects.py` | Routes for `/api/v1/projects` — project CRUD. |
| `v1/contents.py` | Routes for `/api/v1/projects/{id}/contents` — content submission and retrieval. |
| `v1/localization.py` | Routes for `/api/v1/projects/{id}/contents/{id}/localize` — trigger localization pipeline. |
| `v1/translations.py` | Routes for `/api/v1/translations/*` — translation results, version history, version comparison. |
| `v1/analytics.py` | Routes for `/api/v1/analytics/*` — dashboard statistics. |

**Design rule:** Routers call services. They never access repositories or the database directly.

---

### `app/schemas/` — Pydantic Schemas

Defines the contract between the API and its consumers. All request validation and response serialization is handled here.

| File | Purpose |
|---|---|
| `base.py` | Base schema class with shared `model_config` (ORM mode, JSON serialization settings). |
| `auth.py` | `RegisterRequest`, `LoginRequest`, `TokenResponse`, `RefreshRequest`, `LogoutRequest`. |
| `user.py` | `UserResponse`, `UserUpdate`. |
| `project.py` | `ProjectCreate`, `ProjectUpdate`, `ProjectResponse`, `ProjectListResponse`. |
| `content.py` | `ContentCreate`, `ContentResponse`, `ContentListResponse`. |
| `localization.py` | `LocalizeRequest`, `LocalizeResponse`. |
| `translation.py` | `TranslationResponse`, `VersionResponse`, `VersionCompareResponse`. |
| `analytics.py` | `DashboardResponse`, `LanguageUsageStat`, `QualityDistribution`. |
| `common.py` | `PaginatedResponse`, `ErrorResponse`, `MessageResponse`. Reused across all domains. |

**Design rule:** Request schemas never expose internal fields (`id`, `created_at`). Response schemas always include them.

---

### `app/services/` — Service Layer

The sole owner of business logic. Orchestrates repositories, enforces domain rules, coordinates with the localization engine.

| File | Purpose |
|---|---|
| `auth_service.py` | User registration, login, password verification, JWT generation, token refresh, logout/revocation. |
| `user_service.py` | User profile retrieval, update, admin-level user listing, account deactivation. |
| `project_service.py` | Project CRUD with ownership validation, status transitions, soft-delete cascading. |
| `content_service.py` | Content submission with deduplication (hash check), retrieval, status tracking. |
| `localization_service.py` | Orchestrates the full pipeline: detect → translate → adapt → score → persist → version. |
| `translation_service.py` | Translation retrieval, version history, version comparison. |
| `analytics_service.py` | Aggregation queries for dashboard stats, language usage, quality distribution. |

**Design rule:** Services raise domain exceptions (never HTTP exceptions). They never access HTTP request objects or return HTTP responses.

---

### `app/repositories/` — Repository Layer

Abstracts all database access behind a clean interface. Encapsulates SQLAlchemy query construction.

| File | Purpose |
|---|---|
| `base.py` | Generic `BaseRepository[T]` with `get_by_id()`, `get_all()`, `create()`, `update()`, `delete()`, `count()`. |
| `user_repository.py` | `get_by_email()`, `get_by_role()`. |
| `project_repository.py` | `get_by_owner()`, `get_with_stats()`, `search()`. |
| `content_repository.py` | `get_by_project()`, `get_by_hash()`. |
| `translation_repository.py` | `get_by_content()`, `get_by_language_pair()`, `get_latest_by_content()`, `aggregate_quality_scores()`. |
| `version_repository.py` | `get_by_translation()`, `get_latest_version()`, `compare_versions()`. |
| `quality_score_repository.py` | `get_by_translation()`, `upsert()`. |
| `language_repository.py` | `get_all_active()`, `get_by_code()`. |
| `refresh_token_repository.py` | `get_by_hash()`, `revoke_all_for_user()`, `cleanup_expired()`. |

**Design rule:** Repositories receive a SQLAlchemy session via constructor injection. They never manage transactions themselves.

---

### `app/models/` — Database Layer

SQLAlchemy ORM model classes. Each file maps to one database table.

| File | Purpose |
|---|---|
| `base.py` | `Base` declarative base. `TimestampMixin` (adds `created_at`, `updated_at`). `SoftDeleteMixin` (adds `deleted_at`). |
| `user.py` | `User` model → `users` table. |
| `project.py` | `Project` model → `projects` table. |
| `content.py` | `Content` model → `contents` table. |
| `translation.py` | `Translation` model → `translations` table. |
| `quality_score.py` | `QualityScore` model → `quality_scores` table. |
| `translation_version.py` | `TranslationVersion` model → `translation_versions` table. |
| `supported_language.py` | `SupportedLanguage` model → `supported_languages` table. |
| `refresh_token.py` | `RefreshToken` model → `refresh_tokens` table. |
| `audit_log.py` | `AuditLog` model → `audit_logs` table. |
| `__init__.py` | Imports all models so Alembic can discover them for auto-generated migrations. |

**Design rule:** Models define table structure, relationships, and constraints only. No business logic in models.

---

### `app/database/` — Database Configuration

Manages the database connection lifecycle.

| File | Purpose |
|---|---|
| `session.py` | Creates SQLAlchemy `Engine` and `SessionLocal` factory. Configures connection pooling parameters. Provides the `get_db()` generator for dependency injection. |
| `seed.py` | Populates initial reference data on first run: supported languages, default admin account. Idempotent (safe to run multiple times). |

---

### `app/core/` — Cross-Cutting Concerns

Shared utilities and infrastructure that span all layers.

| File | Purpose |
|---|---|
| `security.py` | `hash_password()`, `verify_password()`, `create_access_token()`, `create_refresh_token()`, `decode_token()`. |
| `exceptions.py` | Domain exception hierarchy: `AppException`, `NotFoundException`, `UnauthorizedException`, `ForbiddenException`, `ConflictException`, `ValidationException`. |
| `logging.py` | Structured logging setup. Configures log format, log level, and output handlers. |
| `middleware.py` | CORS middleware configuration. Global error handling middleware (catches domain exceptions → JSON responses). Request/response logging middleware. |

---

### `app/localization/` — AI/NLP Engine

The localization pipeline modules. Each module handles one stage of the pipeline.

| File | Purpose |
|---|---|
| `detector.py` | Language detection. Input: raw text. Output: language code + confidence score. |
| `translator.py` | Translation engine. Input: text + source language + target languages. Output: translated text per language. |
| `adapter.py` | Cultural adaptation. Input: raw translation + locale metadata. Output: culturally adapted text. |
| `scorer.py` | Quality scoring. Input: source + translation. Output: fluency, adequacy, cultural fit, overall scores. |

---

### `alembic/` — Database Migrations

Manages database schema evolution through versioned migration scripts.

| File | Purpose |
|---|---|
| `env.py` | Alembic environment configuration. Connects to the database, imports models for autogeneration. |
| `script.py.mako` | Template for auto-generated migration files. |
| `versions/` | Directory where individual migration scripts are stored chronologically. |

---

### `tests/` — Test Suite

Organized into unit tests (isolated, mocked dependencies) and integration tests (real database, full API stack).

| Directory | Purpose |
|---|---|
| `conftest.py` | Shared fixtures: test database setup/teardown, test client, authenticated user helpers, factory functions. |
| `unit/services/` | Tests each service method in isolation. Dependencies (repositories) are mocked. |
| `unit/repositories/` | Tests each repository method against a test database session. |
| `unit/localization/` | Tests each NLP pipeline module with sample inputs. |
| `integration/` | Tests full API request → response cycles. Uses FastAPI `TestClient` with a real test database. |

---

### Root Configuration Files

| File | Purpose |
|---|---|
| `alembic.ini` | Alembic configuration: database URL, migration directory, logging. |
| `requirements.txt` | Pinned Python dependencies for reproducible installs. |
| `Dockerfile` | Multi-stage Docker image: install deps → copy app → run with Uvicorn. |
| `.env.example` | Template listing all required environment variables with placeholder values. |
| `README.md` | Backend developer guide: setup, running, testing, deployment. |

---

## Layer Dependency Flow

```
api/ ──────────► services/ ──────────► repositories/ ──────────► models/
  │                 │                       │                       │
  │                 │                       │                       │
  ▼                 ▼                       ▼                       ▼
schemas/         core/                  database/              (SQLAlchemy)
(validation)   (security,              (session.py)           (PostgreSQL)
               exceptions,
               middleware)

                services/
                    │
                    ▼
              localization/
              (detector, translator,
               adapter, scorer)
```

**Strict rules:**
* `api/` → calls `services/` only
* `services/` → calls `repositories/` and `localization/`
* `repositories/` → calls `models/` via SQLAlchemy session
* No layer may skip a level (e.g., `api/` must never call `repositories/` directly)
* `core/` is used by all layers
* `schemas/` is used by `api/` layer only
