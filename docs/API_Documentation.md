# API Documentation

This document describes the APIs used in the Marketing Attribution Dashboard project.

**Base URL:** `http://localhost:8000`

---

# 1. Overview

This system is designed to:

- Track user journeys
- Manage marketing campaigns
- Generate attribution reports
- Provide analytics dashboard data

---

# 2. Authentication APIs

## 2.1 Register User

**Endpoint:** `/api/auth/register`

**Method:** `POST`

**Description:** Create a new user account.

### Request Body

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "123456"
}
```

### Response

```json
{
  "message": "User registered successfully"
}
```

---

## 2.2 Login User

**Endpoint:** `/api/auth/login`

**Method:** `POST`

**Description:** Authenticate the user and return a JWT token.

### Request Body

```json
{
  "email": "john@example.com",
  "password": "123456"
}
```

### Response

```json
{
  "token": "jwt_token_here",
  "user": {
    "id": 1,
    "email": "john@example.com"
  }
}
```

---

# 3. Campaign APIs

## 3.1 Get All Campaigns

**Endpoint:** `/api/campaigns`

**Method:** `GET`

**Description:** Retrieve all marketing campaigns.

### Response

```json
[
  {
    "campaign_id": "CAMP001",
    "campaign_name": "Summer Sale",
    "budget": 5000,
    "status": "active"
  }
]
```

---

## 3.2 Create Campaign

**Endpoint:** `/api/campaigns`

**Method:** `POST`

**Description:** Create a new marketing campaign.

### Request Body

```json
{
  "campaign_name": "Winter Sale",
  "budget": 3000
}
```

### Response

```json
{
  "message": "Campaign created successfully"
}
```

---

# 4. Customer Journey APIs

## 4.1 Track User Interaction

**Endpoint:** `/api/journey`

**Method:** `POST`

**Description:** Store customer journey interactions.

### Request Body

```json
{
  "cookie": "abc123",
  "timestamp": "2026-07-06T10:00:00Z",
  "interaction": "click_ad",
  "conversion": 0,
  "revenue": 0
}
```

### Response

```json
{
  "message": "Journey recorded successfully"
}
```

---

## 4.2 Get Customer Journeys

**Endpoint:** `/api/journey`

**Method:** `GET`

**Description:** Retrieve all recorded customer journeys.

### Response

```json
[
  {
    "cookie": "abc123",
    "interaction": "click_ad",
    "timestamp": "2026-07-06T10:00:00Z",
    "conversion": 1,
    "revenue": 1200
  }
]
```

---

# 5. Attribution APIs

## Get Attribution Report

**Endpoint:** `/api/attribution`

**Method:** `GET`

**Description:** Return attribution analysis.

### Response

```json
{
  "first_click": 30,
  "last_click": 40,
  "linear": 20,
  "time_decay": 10
}
```

---

# 6. Analytics APIs

## Dashboard Overview

**Endpoint:** `/api/analytics/overview`

**Method:** `GET`

**Description:** Return dashboard analytics.

### Response

```json
{
  "total_users": 1200,
  "total_conversions": 320,
  "total_revenue": 54000
}
```

---

# 7. Error Handling

The API uses standard HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Resource Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Internal Server Error |

### Error Response

```json
{
  "error": "Something went wrong"
}
```

---

# 8. Authentication Header

Protected endpoints require a JWT token.

```http
Authorization: Bearer <jwt_token>
```

---

# 9. Notes

- All APIs return JSON responses.
- Authentication is handled using JWT tokens.
- This document represents the current API design and may be updated as the project evolves.