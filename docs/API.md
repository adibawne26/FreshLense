# API Documentation

## Overview

FreshLense exposes a RESTful API built with FastAPI.

The API supports:

- User Authentication
- Multi-Factor Authentication (MFA)
- Page Management
- Manual Crawling
- Content Monitoring
- Fact Verification
- Analytics
- AI Services
- Health Monitoring
- Prometheus Metrics

Base URL

```
http://localhost:8000
```

---

# Authentication

## Register

```
POST /auth/register
```

Creates a new user account.

---

## Login

```
POST /auth/login
```

Authenticates a user and returns a JWT access token.

---

## Validate Token

```
POST /auth/validate-token
```

Verifies whether the provided JWT token is valid.

---

## MFA

Available endpoints include:

```
POST /auth/send-mfa-code

POST /auth/verify-mfa

POST /auth/setup-mfa

POST /auth/disable-mfa

POST /auth/check-mfa-session
```

---

# User

Retrieve authenticated user information.

```
GET /user/profile
```

---

# Page Management

## Create Page

```
POST /api/pages
```

Adds a webpage for monitoring.

---

## List Pages

```
GET /api/pages
```

Returns all tracked pages.

---

## Get Page

```
GET /api/pages/{page_id}
```

---

## Delete Page

```
DELETE /api/pages/{page_id}
```

---

## Find by URL

```
GET /api/pages/by-url
```

Checks whether a page is already being monitored.

---

# Crawling

Manual crawl:

```
POST /api/crawl/{page_id}
```

Performs an immediate crawl and stores a new version if significant changes are detected.

---

# Fact Verification

## Check

```
POST /fact-check/check
```

Runs AI-assisted fact verification.

---

## Direct Check

```
POST /fact-check/check-direct
```

Fact checks manually supplied content.

---

## Compare

```
POST /fact-check/compare
```

Compares two content versions.

---

# Analytics

```
GET /analytics
```

Returns analytics data used by the dashboard.

---

# Health

```
GET /health
```

Returns application health.

---

# Metrics

```
GET /metrics
```

Prometheus metrics endpoint.

Exposes:

- Crawl Requests
- Crawl Success
- Crawl Failures
- Crawl Duration
- HTTP Metrics

---

# AI Services

```
GET /api/ai/status
```

Returns AI service configuration and availability.

---

# Response Codes

| Code | Meaning |
|------:|---------|
| 200 | Success |
| 201 | Resource Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

# Interactive API Documentation

FastAPI automatically generates Swagger UI.

```
http://localhost:8000/docs
```

ReDoc is also available.

```
http://localhost:8000/redoc
```

These interfaces provide live API testing, request schemas, and response models.