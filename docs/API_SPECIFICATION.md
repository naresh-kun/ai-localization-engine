# API Specification

## AI-Powered Multilingual Content Localization Engine

**Base URL:** `/api/v1`

**Content Type:** `application/json`

**Authentication:** Bearer JWT token in `Authorization` header unless marked as Public.

---

## Table of Contents

1. [Authentication APIs](#1-authentication-apis)
2. [Project APIs](#2-project-apis)
3. [Content APIs](#3-content-apis)
4. [Localization APIs](#4-localization-apis)
5. [Analytics APIs](#5-analytics-apis)
6. [Common Response Formats](#6-common-response-formats)

---

## 1. Authentication APIs

### 1.1 Register

Create a new user account.

| Property | Value |
|---|---|
| **URL** | `/api/v1/auth/register` |
| **Method** | `POST` |
| **Auth Required** | No (Public) |

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "SecureP@ss123",
  "full_name": "Naresh Kumar"
}
```

| Field | Type | Required | Constraints |
|---|---|---|---|
| `email` | `string` | Yes | Valid email format, max 255 chars |
| `password` | `string` | Yes | Min 8 chars, must contain uppercase, lowercase, number, and special character |
| `full_name` | `string` | Yes | Min 2 chars, max 150 chars |

**Response Body (201 Created):**

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "email": "user@example.com",
  "full_name": "Naresh Kumar",
  "role": "user",
  "is_active": true,
  "created_at": "2026-06-06T10:30:00Z",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Status Codes:**

| Code | Condition |
|---|---|
| `201 Created` | Account created successfully |
| `409 Conflict` | Email already registered |
| `422 Unprocessable Entity` | Validation error (invalid email, weak password, etc.) |

---

### 1.2 Login

Authenticate an existing user and receive JWT tokens.

| Property | Value |
|---|---|
| **URL** | `/api/v1/auth/login` |
| **Method** | `POST` |
| **Auth Required** | No (Public) |

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "SecureP@ss123"
}
```

| Field | Type | Required | Constraints |
|---|---|---|---|
| `email` | `string` | Yes | Valid email format |
| `password` | `string` | Yes | Non-empty |

**Response Body (200 OK):**

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "email": "user@example.com",
  "full_name": "Naresh Kumar",
  "role": "user",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Status Codes:**

| Code | Condition |
|---|---|
| `200 OK` | Login successful |
| `401 Unauthorized` | Invalid email or password |
| `403 Forbidden` | Account is deactivated (`is_active = false`) |
| `422 Unprocessable Entity` | Validation error |

---

### 1.3 Refresh Token

Exchange a valid refresh token for a new access token and rotated refresh token.

| Property | Value |
|---|---|
| **URL** | `/api/v1/auth/refresh` |
| **Method** | `POST` |
| **Auth Required** | No (Public — uses refresh token in body) |

**Request Body:**

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

| Field | Type | Required | Constraints |
|---|---|---|---|
| `refresh_token` | `string` | Yes | Valid, non-expired, non-revoked refresh JWT |

**Response Body (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Status Codes:**

| Code | Condition |
|---|---|
| `200 OK` | Token refreshed successfully |
| `401 Unauthorized` | Refresh token is invalid, expired, or revoked |

---

### 1.4 Logout

Revoke the current refresh token, invalidating the session.

| Property | Value |
|---|---|
| **URL** | `/api/v1/auth/logout` |
| **Method** | `POST` |
| **Auth Required** | Yes (Bearer token) |

**Request Body:**

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

| Field | Type | Required | Constraints |
|---|---|---|---|
| `refresh_token` | `string` | Yes | The refresh token to revoke |

**Response Body (200 OK):**

```json
{
  "message": "Successfully logged out."
}
```

**Status Codes:**

| Code | Condition |
|---|---|
| `200 OK` | Logout successful, token revoked |
| `401 Unauthorized` | Access token missing or invalid |

---

## 2. Project APIs

### 2.1 Create Project

Create a new localization project for the authenticated user.

| Property | Value |
|---|---|
| **URL** | `/api/v1/projects` |
| **Method** | `POST` |
| **Auth Required** | Yes (Bearer token) |

**Request Body:**

```json
{
  "name": "Mobile App v2 Localization",
  "description": "Localize all UI strings for the mobile app version 2 release.",
  "source_language": "en"
}
```

| Field | Type | Required | Constraints |
|---|---|---|---|
| `name` | `string` | Yes | Min 3 chars, max 255 chars |
| `description` | `string` | No | Max 2000 chars |
| `source_language` | `string` | Yes | Must be a valid ISO 639-1 code from `supported_languages` |

**Response Body (201 Created):**

```json
{
  "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "name": "Mobile App v2 Localization",
  "description": "Localize all UI strings for the mobile app version 2 release.",
  "source_language": "en",
  "status": "active",
  "owner_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "created_at": "2026-06-06T10:45:00Z",
  "updated_at": "2026-06-06T10:45:00Z"
}
```

**Status Codes:**

| Code | Condition |
|---|---|
| `201 Created` | Project created successfully |
| `401 Unauthorized` | Missing or invalid access token |
| `422 Unprocessable Entity` | Validation error (invalid language code, missing name, etc.) |

---

### 2.2 Get Projects

Retrieve a paginated list of projects owned by the authenticated user.

| Property | Value |
|---|---|
| **URL** | `/api/v1/projects` |
| **Method** | `GET` |
| **Auth Required** | Yes (Bearer token) |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `page` | `integer` | No | `1` | Page number (1-indexed) |
| `per_page` | `integer` | No | `20` | Items per page (max 100) |
| `status` | `string` | No | — | Filter by status: `active`, `archived` |
| `search` | `string` | No | — | Search project name (partial match) |
| `sort_by` | `string` | No | `created_at` | Sort field: `created_at`, `updated_at`, `name` |
| `sort_order` | `string` | No | `desc` | Sort direction: `asc`, `desc` |

**Response Body (200 OK):**

```json
{
  "items": [
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "name": "Mobile App v2 Localization",
      "description": "Localize all UI strings for the mobile app version 2 release.",
      "source_language": "en",
      "status": "active",
      "owner_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "content_count": 42,
      "created_at": "2026-06-06T10:45:00Z",
      "updated_at": "2026-06-06T10:45:00Z"
    }
  ],
  "total": 15,
  "page": 1,
  "per_page": 20,
  "total_pages": 1
}
```

**Status Codes:**

| Code | Condition |
|---|---|
| `200 OK` | Projects retrieved successfully |
| `401 Unauthorized` | Missing or invalid access token |
| `422 Unprocessable Entity` | Invalid query parameters |

---

### 2.3 Update Project

Update an existing project's metadata. Only the project owner can update it.

| Property | Value |
|---|---|
| **URL** | `/api/v1/projects/{project_id}` |
| **Method** | `PATCH` |
| **Auth Required** | Yes (Bearer token) |

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `project_id` | `UUID` | ID of the project to update |

**Request Body (all fields optional):**

```json
{
  "name": "Mobile App v2.1 Localization",
  "description": "Updated scope to include accessibility strings.",
  "source_language": "en",
  "status": "archived"
}
```

| Field | Type | Required | Constraints |
|---|---|---|---|
| `name` | `string` | No | Min 3 chars, max 255 chars |
| `description` | `string` | No | Max 2000 chars |
| `source_language` | `string` | No | Valid ISO 639-1 code from `supported_languages` |
| `status` | `string` | No | `active` or `archived` |

**Response Body (200 OK):**

```json
{
  "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "name": "Mobile App v2.1 Localization",
  "description": "Updated scope to include accessibility strings.",
  "source_language": "en",
  "status": "archived",
  "owner_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "created_at": "2026-06-06T10:45:00Z",
  "updated_at": "2026-06-06T11:20:00Z"
}
```

**Status Codes:**

| Code | Condition |
|---|---|
| `200 OK` | Project updated successfully |
| `401 Unauthorized` | Missing or invalid access token |
| `403 Forbidden` | User is not the project owner |
| `404 Not Found` | Project does not exist |
| `422 Unprocessable Entity` | Validation error |

---

### 2.4 Delete Project

Soft-delete a project and all its associated content. Only the project owner can delete it.

| Property | Value |
|---|---|
| **URL** | `/api/v1/projects/{project_id}` |
| **Method** | `DELETE` |
| **Auth Required** | Yes (Bearer token) |

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `project_id` | `UUID` | ID of the project to delete |

**Response Body (200 OK):**

```json
{
  "message": "Project deleted successfully.",
  "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901"
}
```

**Status Codes:**

| Code | Condition |
|---|---|
| `200 OK` | Project soft-deleted successfully |
| `401 Unauthorized` | Missing or invalid access token |
| `403 Forbidden` | User is not the project owner |
| `404 Not Found` | Project does not exist |

---

## 3. Content APIs

### 3.1 Submit Content

Submit source text content to a project for localization.

| Property | Value |
|---|---|
| **URL** | `/api/v1/projects/{project_id}/contents` |
| **Method** | `POST` |
| **Auth Required** | Yes (Bearer token) |

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `project_id` | `UUID` | ID of the parent project |

**Request Body:**

```json
{
  "source_text": "Welcome to our platform. We help businesses reach global audiences with culturally adapted content.",
  "source_language": "en",
  "metadata": {
    "content_type": "marketing_copy",
    "tags": ["homepage", "hero_section"],
    "notes": "Maintain professional but friendly tone."
  }
}
```

| Field | Type | Required | Constraints |
|---|---|---|---|
| `source_text` | `string` | Yes | Min 1 char, max 50000 chars |
| `source_language` | `string` | No | ISO 639-1 code. Defaults to project's `source_language` if omitted |
| `metadata` | `object` | No | Arbitrary JSON. Max 10KB |

**Response Body (201 Created):**

```json
{
  "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "project_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "source_text": "Welcome to our platform. We help businesses reach global audiences with culturally adapted content.",
  "source_language": "en",
  "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "status": "pending",
  "metadata": {
    "content_type": "marketing_copy",
    "tags": ["homepage", "hero_section"],
    "notes": "Maintain professional but friendly tone."
  },
  "created_at": "2026-06-06T11:00:00Z",
  "updated_at": "2026-06-06T11:00:00Z"
}
```

**Status Codes:**

| Code | Condition |
|---|---|
| `201 Created` | Content submitted successfully |
| `401 Unauthorized` | Missing or invalid access token |
| `403 Forbidden` | User does not own the project |
| `404 Not Found` | Project does not exist |
| `409 Conflict` | Duplicate content (same `content_hash` already exists in this project) |
| `422 Unprocessable Entity` | Validation error (empty text, invalid language code) |

---

### 3.2 Get Content

Retrieve content items for a project. Supports fetching a single item or a paginated list.

#### 3.2.1 Get Single Content

| Property | Value |
|---|---|
| **URL** | `/api/v1/projects/{project_id}/contents/{content_id}` |
| **Method** | `GET` |
| **Auth Required** | Yes (Bearer token) |

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `project_id` | `UUID` | ID of the parent project |
| `content_id` | `UUID` | ID of the content item |

**Response Body (200 OK):**

```json
{
  "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "project_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "source_text": "Welcome to our platform. We help businesses reach global audiences with culturally adapted content.",
  "source_language": "en",
  "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "status": "completed",
  "metadata": {
    "content_type": "marketing_copy",
    "tags": ["homepage", "hero_section"],
    "notes": "Maintain professional but friendly tone."
  },
  "translations": [
    {
      "id": "d4e5f6a7-b8c9-0123-defa-234567890123",
      "target_language": "ta",
      "status": "completed",
      "current_version": 1
    },
    {
      "id": "e5f6a7b8-c9d0-1234-efab-345678901234",
      "target_language": "fr",
      "status": "completed",
      "current_version": 2
    }
  ],
  "created_at": "2026-06-06T11:00:00Z",
  "updated_at": "2026-06-06T11:15:00Z"
}
```

#### 3.2.2 List Contents

| Property | Value |
|---|---|
| **URL** | `/api/v1/projects/{project_id}/contents` |
| **Method** | `GET` |
| **Auth Required** | Yes (Bearer token) |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `page` | `integer` | No | `1` | Page number |
| `per_page` | `integer` | No | `20` | Items per page (max 100) |
| `status` | `string` | No | — | Filter: `pending`, `processing`, `completed`, `failed` |

**Response Body (200 OK):**

```json
{
  "items": [
    {
      "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
      "source_text": "Welcome to our platform...",
      "source_language": "en",
      "status": "completed",
      "translation_count": 2,
      "created_at": "2026-06-06T11:00:00Z",
      "updated_at": "2026-06-06T11:15:00Z"
    }
  ],
  "total": 42,
  "page": 1,
  "per_page": 20,
  "total_pages": 3
}
```

**Status Codes (both endpoints):**

| Code | Condition |
|---|---|
| `200 OK` | Content retrieved successfully |
| `401 Unauthorized` | Missing or invalid access token |
| `403 Forbidden` | User does not own the project |
| `404 Not Found` | Project or content does not exist |

---

## 4. Localization APIs

### 4.1 Start Localization

Trigger the localization pipeline for a content item. Runs language detection, translation, cultural adaptation, and quality scoring for each target language.

| Property | Value |
|---|---|
| **URL** | `/api/v1/projects/{project_id}/contents/{content_id}/localize` |
| **Method** | `POST` |
| **Auth Required** | Yes (Bearer token) |

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `project_id` | `UUID` | ID of the parent project |
| `content_id` | `UUID` | ID of the content to localize |

**Request Body:**

```json
{
  "target_languages": ["ta", "fr", "de"],
  "options": {
    "formality": "formal",
    "preserve_formatting": true
  }
}
```

| Field | Type | Required | Constraints |
|---|---|---|---|
| `target_languages` | `string[]` | Yes | Min 1 language, each must be a valid ISO 639-1 code from `supported_languages`, cannot include the source language |
| `options` | `object` | No | Localization options |
| `options.formality` | `string` | No | `formal`, `neutral`, `informal`. Default: `neutral` |
| `options.preserve_formatting` | `boolean` | No | Whether to preserve structural formatting. Default: `true` |

**Response Body (202 Accepted):**

```json
{
  "content_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "status": "processing",
  "target_languages": ["ta", "fr", "de"],
  "translations": [
    {
      "id": "d4e5f6a7-b8c9-0123-defa-234567890123",
      "target_language": "ta",
      "status": "pending"
    },
    {
      "id": "e5f6a7b8-c9d0-1234-efab-345678901234",
      "target_language": "fr",
      "status": "pending"
    },
    {
      "id": "f6a7b8c9-d0e1-2345-fabc-456789012345",
      "target_language": "de",
      "status": "pending"
    }
  ],
  "initiated_at": "2026-06-06T11:30:00Z"
}
```

**Status Codes:**

| Code | Condition |
|---|---|
| `202 Accepted` | Localization pipeline initiated |
| `401 Unauthorized` | Missing or invalid access token |
| `403 Forbidden` | User does not own the project |
| `404 Not Found` | Project or content does not exist |
| `409 Conflict` | Localization already in progress for this content with the same target languages |
| `422 Unprocessable Entity` | Validation error (invalid language codes, target includes source language) |

---

### 4.2 Get Translation

Retrieve the full translation result for a specific content-language pair.

| Property | Value |
|---|---|
| **URL** | `/api/v1/translations/{translation_id}` |
| **Method** | `GET` |
| **Auth Required** | Yes (Bearer token) |

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `translation_id` | `UUID` | ID of the translation |

**Response Body (200 OK):**

```json
{
  "id": "d4e5f6a7-b8c9-0123-defa-234567890123",
  "content_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "source_language": "en",
  "target_language": "ta",
  "raw_translation": "எங்கள் தளத்திற்கு வருக. உலகளாவிய பார்வையாளர்களை...",
  "adapted_translation": "எங்கள் தளத்திற்கு வரவேற்கிறோம். உலகளாவிய பார்வையாளர்களை...",
  "status": "completed",
  "current_version": 1,
  "quality_scores": {
    "fluency_score": 0.92,
    "adequacy_score": 0.88,
    "cultural_fit_score": 0.85,
    "overall_score": 0.88
  },
  "created_at": "2026-06-06T11:30:00Z",
  "updated_at": "2026-06-06T11:32:00Z"
}
```

**Status Codes:**

| Code | Condition |
|---|---|
| `200 OK` | Translation retrieved successfully |
| `401 Unauthorized` | Missing or invalid access token |
| `403 Forbidden` | User does not own the parent project |
| `404 Not Found` | Translation does not exist |

---

### 4.3 Get Translation History

Retrieve all version snapshots for a translation, enabling review of how a translation has evolved over re-translation cycles.

| Property | Value |
|---|---|
| **URL** | `/api/v1/translations/{translation_id}/versions` |
| **Method** | `GET` |
| **Auth Required** | Yes (Bearer token) |

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `translation_id` | `UUID` | ID of the translation |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `page` | `integer` | No | `1` | Page number |
| `per_page` | `integer` | No | `20` | Items per page (max 100) |
| `sort_order` | `string` | No | `desc` | Sort by version number: `asc`, `desc` |

**Response Body (200 OK):**

```json
{
  "translation_id": "d4e5f6a7-b8c9-0123-defa-234567890123",
  "source_language": "en",
  "target_language": "ta",
  "items": [
    {
      "id": "11111111-aaaa-bbbb-cccc-dddddddddddd",
      "version_number": 2,
      "translated_content": "எங்கள் தளத்திற்கு வரவேற்கிறோம்...",
      "adapted_content": "எங்கள் தளத்திற்கு வரவேற்கிறோம்...",
      "source_content_hash": "e3b0c44298fc1c149afbf4c8996fb924...",
      "quality_snapshot": {
        "fluency_score": 0.94,
        "adequacy_score": 0.91,
        "cultural_fit_score": 0.88,
        "overall_score": 0.91
      },
      "created_at": "2026-06-07T09:00:00Z"
    },
    {
      "id": "22222222-aaaa-bbbb-cccc-dddddddddddd",
      "version_number": 1,
      "translated_content": "எங்கள் தளத்திற்கு வருக...",
      "adapted_content": "எங்கள் தளத்திற்கு வரவேற்கிறோம்...",
      "source_content_hash": "e3b0c44298fc1c149afbf4c8996fb924...",
      "quality_snapshot": {
        "fluency_score": 0.92,
        "adequacy_score": 0.88,
        "cultural_fit_score": 0.85,
        "overall_score": 0.88
      },
      "created_at": "2026-06-06T11:32:00Z"
    }
  ],
  "total": 2,
  "page": 1,
  "per_page": 20,
  "total_pages": 1
}
```

**Status Codes:**

| Code | Condition |
|---|---|
| `200 OK` | Version history retrieved successfully |
| `401 Unauthorized` | Missing or invalid access token |
| `403 Forbidden` | User does not own the parent project |
| `404 Not Found` | Translation does not exist |

---

### 4.4 Compare Versions

Compare two version snapshots of the same translation side-by-side.

| Property | Value |
|---|---|
| **URL** | `/api/v1/translations/{translation_id}/versions/compare` |
| **Method** | `GET` |
| **Auth Required** | Yes (Bearer token) |

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `translation_id` | `UUID` | ID of the translation |

**Query Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `version_a` | `integer` | Yes | First version number to compare |
| `version_b` | `integer` | Yes | Second version number to compare |

**Response Body (200 OK):**

```json
{
  "translation_id": "d4e5f6a7-b8c9-0123-defa-234567890123",
  "version_a": {
    "version_number": 1,
    "translated_content": "எங்கள் தளத்திற்கு வருக...",
    "adapted_content": "எங்கள் தளத்திற்கு வரவேற்கிறோம்...",
    "quality_snapshot": {
      "fluency_score": 0.92,
      "adequacy_score": 0.88,
      "cultural_fit_score": 0.85,
      "overall_score": 0.88
    },
    "source_content_hash": "e3b0c44298fc1c149afbf4c8996fb924...",
    "created_at": "2026-06-06T11:32:00Z"
  },
  "version_b": {
    "version_number": 2,
    "translated_content": "எங்கள் தளத்திற்கு வரவேற்கிறோம்...",
    "adapted_content": "எங்கள் தளத்திற்கு வரவேற்கிறோம்...",
    "quality_snapshot": {
      "fluency_score": 0.94,
      "adequacy_score": 0.91,
      "cultural_fit_score": 0.88,
      "overall_score": 0.91
    },
    "source_content_hash": "e3b0c44298fc1c149afbf4c8996fb924...",
    "created_at": "2026-06-07T09:00:00Z"
  },
  "quality_diff": {
    "fluency_score": 0.02,
    "adequacy_score": 0.03,
    "cultural_fit_score": 0.03,
    "overall_score": 0.03
  },
  "source_changed": false
}
```

**Status Codes:**

| Code | Condition |
|---|---|
| `200 OK` | Comparison generated successfully |
| `401 Unauthorized` | Missing or invalid access token |
| `403 Forbidden` | User does not own the parent project |
| `404 Not Found` | Translation or one of the version numbers does not exist |
| `422 Unprocessable Entity` | Missing or invalid version numbers, or both versions are the same |

---

## 5. Analytics APIs

### 5.1 Dashboard Statistics

Retrieve aggregated statistics for the authenticated user's dashboard. Admins receive system-wide stats; standard users receive stats scoped to their own projects.

| Property | Value |
|---|---|
| **URL** | `/api/v1/analytics/dashboard` |
| **Method** | `GET` |
| **Auth Required** | Yes (Bearer token) |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `project_id` | `UUID` | No | — | Scope stats to a specific project. Omit for aggregate stats across all projects |
| `date_from` | `string` | No | 30 days ago | Start date filter (ISO 8601: `YYYY-MM-DD`) |
| `date_to` | `string` | No | today | End date filter (ISO 8601: `YYYY-MM-DD`) |

**Response Body (200 OK):**

```json
{
  "summary": {
    "total_projects": 8,
    "total_contents": 342,
    "total_translations": 1026,
    "active_projects": 5,
    "archived_projects": 3
  },
  "localization_stats": {
    "completed_translations": 980,
    "pending_translations": 30,
    "failed_translations": 16,
    "average_quality_score": 0.87
  },
  "language_usage": [
    {
      "language_code": "ta",
      "language_name": "Tamil",
      "translation_count": 342,
      "average_quality_score": 0.85
    },
    {
      "language_code": "fr",
      "language_name": "French",
      "translation_count": 342,
      "average_quality_score": 0.91
    },
    {
      "language_code": "de",
      "language_name": "German",
      "translation_count": 342,
      "average_quality_score": 0.86
    }
  ],
  "quality_distribution": {
    "excellent": 420,
    "good": 380,
    "acceptable": 140,
    "poor": 40
  },
  "recent_activity": [
    {
      "date": "2026-06-06",
      "translations_completed": 45,
      "contents_submitted": 12
    },
    {
      "date": "2026-06-05",
      "translations_completed": 38,
      "contents_submitted": 8
    }
  ],
  "date_range": {
    "from": "2026-05-07",
    "to": "2026-06-06"
  }
}
```

**Quality Distribution Thresholds:**

| Category | Score Range |
|---|---|
| Excellent | 0.90 – 1.00 |
| Good | 0.75 – 0.89 |
| Acceptable | 0.50 – 0.74 |
| Poor | 0.00 – 0.49 |

**Status Codes:**

| Code | Condition |
|---|---|
| `200 OK` | Statistics retrieved successfully |
| `401 Unauthorized` | Missing or invalid access token |
| `403 Forbidden` | User does not own the specified project |
| `404 Not Found` | Specified project does not exist |
| `422 Unprocessable Entity` | Invalid date format or range |

---

## 6. Common Response Formats

### 6.1 Error Response

All error responses follow a consistent structure:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Project with id 'b2c3d4e5-f6a7-8901-bcde-f12345678901' not found.",
    "details": null
  }
}
```

| Field | Type | Description |
|---|---|---|
| `error.code` | `string` | Machine-readable error code |
| `error.message` | `string` | Human-readable error description |
| `error.details` | `object \| null` | Additional error context (validation errors, field-level issues) |

### Error Code Registry

| Error Code | HTTP Status | Description |
|---|---|---|
| `VALIDATION_ERROR` | 422 | Request body or query parameter validation failed |
| `UNAUTHORIZED` | 401 | Missing, invalid, or expired access token |
| `FORBIDDEN` | 403 | User lacks permission for the requested action |
| `RESOURCE_NOT_FOUND` | 404 | Requested resource does not exist |
| `CONFLICT` | 409 | Resource conflict (duplicate email, duplicate content, etc.) |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

### 6.2 Validation Error Detail

When a `422` error occurs, the `details` field contains field-level errors:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format."
      },
      {
        "field": "password",
        "message": "Password must be at least 8 characters."
      }
    ]
  }
}
```

### 6.3 Paginated Response

All list endpoints follow the same pagination wrapper:

```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "per_page": 20,
  "total_pages": 0
}
```

| Field | Type | Description |
|---|---|---|
| `items` | `array` | Array of resource objects for the current page |
| `total` | `integer` | Total number of matching resources across all pages |
| `page` | `integer` | Current page number (1-indexed) |
| `per_page` | `integer` | Number of items per page |
| `total_pages` | `integer` | Total number of pages |

### 6.4 Authentication Headers

All protected endpoints require the following header:

```
Authorization: Bearer <access_token>
```

If the token is missing, malformed, or expired, the API returns:

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Access token is missing or invalid."
  }
}
```

---

## Endpoint Summary

| # | Method | Endpoint | Auth | Description |
|---|---|---|---|---|
| 1 | `POST` | `/api/v1/auth/register` | Public | Create new user account |
| 2 | `POST` | `/api/v1/auth/login` | Public | Authenticate and receive tokens |
| 3 | `POST` | `/api/v1/auth/refresh` | Public | Exchange refresh token for new tokens |
| 4 | `POST` | `/api/v1/auth/logout` | Bearer | Revoke refresh token |
| 5 | `POST` | `/api/v1/projects` | Bearer | Create a new project |
| 6 | `GET` | `/api/v1/projects` | Bearer | List user's projects (paginated) |
| 7 | `PATCH` | `/api/v1/projects/{project_id}` | Bearer | Update a project |
| 8 | `DELETE` | `/api/v1/projects/{project_id}` | Bearer | Soft-delete a project |
| 9 | `POST` | `/api/v1/projects/{project_id}/contents` | Bearer | Submit content to a project |
| 10 | `GET` | `/api/v1/projects/{project_id}/contents/{content_id}` | Bearer | Get a single content item |
| 11 | `GET` | `/api/v1/projects/{project_id}/contents` | Bearer | List project contents (paginated) |
| 12 | `POST` | `/api/v1/projects/{project_id}/contents/{content_id}/localize` | Bearer | Start localization pipeline |
| 13 | `GET` | `/api/v1/translations/{translation_id}` | Bearer | Get translation result |
| 14 | `GET` | `/api/v1/translations/{translation_id}/versions` | Bearer | Get translation version history |
| 15 | `GET` | `/api/v1/translations/{translation_id}/versions/compare` | Bearer | Compare two versions |
| 16 | `GET` | `/api/v1/analytics/dashboard` | Bearer | Get dashboard statistics |
