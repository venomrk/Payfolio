# Payfolio - API Design

## Overview
RESTful API design for Payfolio backend built with FastAPI.

**Base URL:** `https://api.payfolio.app/v1`

---

## Authentication

### Auth Flow (NextAuth + Supabase)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│   NextAuth  │───▶│  Supabase   │
│  (Next.js)  │◀───│   (JWT)     │◀───│    Auth     │
└─────────────┘    └─────────────┘    └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │   FastAPI   │
                   │  (Backend)  │
                   └─────────────┘
```

### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

---

## API Endpoints

### 🔐 Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create new account |
| POST | `/auth/login` | Email/password login |
| POST | `/auth/google` | Google OAuth login |
| POST | `/auth/otp/send` | Send phone OTP |
| POST | `/auth/otp/verify` | Verify phone OTP |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/logout` | Invalidate session |
| GET | `/auth/me` | Get current user |

#### POST `/auth/register`
```json
// Request
{
  "email": "user@example.com",
  "password": "securePassword123",
  "full_name": "Rakshit Kumar"
}

// Response 201
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "Rakshit Kumar",
  "plan": "free",
  "access_token": "jwt...",
  "refresh_token": "jwt..."
}
```

#### POST `/auth/login`
```json
// Request
{
  "email": "user@example.com",
  "password": "securePassword123"
}

// Response 200
{
  "access_token": "jwt...",
  "refresh_token": "jwt...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "Rakshit Kumar",
    "plan": "pro"
  }
}
```

---

### 👤 Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Get current user profile |
| PATCH | `/users/me` | Update profile |
| DELETE | `/users/me` | Delete account |
| GET | `/users/me/portfolio` | Get portfolio summary |

#### GET `/users/me/portfolio`
```json
// Response 200
{
  "net_worth": 12345678.00,
  "net_worth_change": 234567.00,
  "net_worth_change_percent": 1.9,
  "total_assets": 13500000.00,
  "total_liabilities": 1154322.00,
  "breakdown": {
    "banks": 1850000.00,
    "investments": 8920000.00,
    "crypto": 1200000.00,
    "wallets": 530000.00,
    "manual_assets": 1000000.00
  },
  "connected_accounts": 8,
  "last_updated": "2026-01-10T10:00:00Z"
}
```

---

### 🏦 Accounts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts` | List all accounts |
| POST | `/accounts` | Add new account |
| GET | `/accounts/{id}` | Get account details |
| PATCH | `/accounts/{id}` | Update account |
| DELETE | `/accounts/{id}` | Remove account |
| POST | `/accounts/{id}/sync` | Force sync account |
| POST | `/accounts/connect/{provider}` | Connect via provider |

#### GET `/accounts`
```json
// Response 200
{
  "accounts": [
    {
      "id": "uuid",
      "name": "HDFC Savings",
      "institution": "HDFC Bank",
      "account_type": "bank",
      "current_balance": 234567.89,
      "currency": "INR",
      "connection_type": "manual",
      "last_synced_at": "2026-01-10T08:00:00Z",
      "sync_status": "ok"
    }
  ],
  "total": 8,
  "by_type": {
    "bank": 3,
    "investment": 2,
    "wallet": 2,
    "crypto": 1
  }
}
```

#### POST `/accounts`
```json
// Request
{
  "name": "HDFC Savings",
  "institution": "HDFC Bank",
  "account_type": "bank",
  "current_balance": 234567.89,
  "currency": "INR"
}

// Response 201
{
  "id": "uuid",
  "name": "HDFC Savings",
  ...
}
```

#### POST `/accounts/connect/zerodha`
```json
// Request
{
  "api_key": "xxx",
  "api_secret": "xxx"
}

// Response 200
{
  "account_id": "uuid",
  "status": "connected",
  "holdings": 45,
  "total_value": 4580000.00
}
```

---

### 💳 Transactions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/transactions` | List transactions |
| POST | `/transactions` | Add manual transaction |
| GET | `/transactions/{id}` | Get transaction |
| PATCH | `/transactions/{id}` | Update transaction |
| DELETE | `/transactions/{id}` | Delete transaction |
| POST | `/transactions/import` | Import from CSV |
| GET | `/transactions/stats` | Transaction statistics |

#### GET `/transactions`
```json
// Query params: ?account_id=&category_id=&from=&to=&type=&limit=50&offset=0

// Response 200
{
  "transactions": [
    {
      "id": "uuid",
      "account_id": "uuid",
      "account_name": "HDFC Savings",
      "amount": -4299.00,
      "transaction_type": "debit",
      "description": "Amazon India",
      "category": {
        "id": 6,
        "name": "Shopping",
        "icon": "🛒"
      },
      "merchant_name": "Amazon India",
      "transaction_date": "2026-01-10",
      "is_recurring": false
    }
  ],
  "total": 1250,
  "limit": 50,
  "offset": 0
}
```

#### GET `/transactions/stats`
```json
// Query params: ?from=2026-01-01&to=2026-01-31

// Response 200
{
  "period": {
    "from": "2026-01-01",
    "to": "2026-01-31"
  },
  "total_income": 145000.00,
  "total_expenses": 67500.00,
  "net_cash_flow": 77500.00,
  "by_category": [
    {"category": "Salary", "amount": 120000.00, "percent": 82.7},
    {"category": "Freelance", "amount": 25000.00, "percent": 17.3}
  ],
  "top_merchants": [
    {"name": "Swiggy", "amount": 8500.00, "count": 23},
    {"name": "Amazon", "amount": 12400.00, "count": 8}
  ]
}
```

---

### 💰 Assets (Manual)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/assets` | List manual assets |
| POST | `/assets` | Add asset |
| PATCH | `/assets/{id}` | Update asset |
| DELETE | `/assets/{id}` | Remove asset |

#### POST `/assets`
```json
// Request
{
  "name": "Flat in Bangalore",
  "asset_type": "real_estate",
  "current_value": 8500000.00,
  "purchase_value": 6500000.00,
  "purchase_date": "2023-06-15"
}

// Response 201
{
  "id": "uuid",
  "name": "Flat in Bangalore",
  "asset_type": "real_estate",
  "current_value": 8500000.00,
  "gain": 2000000.00,
  "gain_percent": 30.77
}
```

---

### 📉 Liabilities

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/liabilities` | List all liabilities |
| POST | `/liabilities` | Add liability |
| PATCH | `/liabilities/{id}` | Update liability |
| DELETE | `/liabilities/{id}` | Remove liability |

#### GET `/liabilities`
```json
// Response 200
{
  "liabilities": [
    {
      "id": "uuid",
      "name": "Home Loan",
      "liability_type": "home_loan",
      "principal_amount": 5000000.00,
      "current_balance": 4200000.00,
      "emi_amount": 42000.00,
      "interest_rate": 8.5,
      "lender": "SBI",
      "paid_percent": 16.0
    }
  ],
  "total_liability": 4200000.00,
  "monthly_emi_total": 42000.00
}
```

---

### ✨ Insights (AI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/insights` | Get active insights |
| GET | `/insights/{id}` | Get insight details |
| POST | `/insights/{id}/dismiss` | Dismiss insight |
| POST | `/insights/{id}/read` | Mark as read |
| POST | `/insights/generate` | Force regenerate |

#### GET `/insights`
```json
// Response 200
{
  "insights": [
    {
      "id": "uuid",
      "insight_type": "cash_runway",
      "title": "Cash Runway Alert",
      "description": "Your cash runway is 4.2 months based on current burn rate of ₹1.2L/month.",
      "severity": "warning",
      "priority": 8,
      "data": {
        "runway_months": 4.2,
        "monthly_burn": 120000.00,
        "available_cash": 504000.00
      },
      "cta_text": "View Cash Flow",
      "cta_link": "/transactions?view=cashflow",
      "is_read": false,
      "created_at": "2026-01-10T06:00:00Z"
    }
  ],
  "unread_count": 3
}
```

#### POST `/insights/generate`
```json
// Request
{
  "types": ["cash_runway", "spending_alert", "subscription_review"]
}

// Response 200
{
  "generated": 3,
  "insights": [...]
}
```

---

### 📈 Net Worth History

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/networth/history` | Get historical data |
| GET | `/networth/current` | Get current snapshot |

#### GET `/networth/history`
```json
// Query: ?from=2025-01-01&to=2026-01-10&interval=month

// Response 200
{
  "history": [
    {"date": "2025-01-31", "net_worth": 8500000.00},
    {"date": "2025-02-28", "net_worth": 8750000.00},
    ...
    {"date": "2026-01-10", "net_worth": 12345678.00}
  ],
  "growth": {
    "absolute": 3845678.00,
    "percent": 45.2
  }
}
```

---

### 💳 Subscriptions (Billing)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/billing/subscription` | Get current plan |
| POST | `/billing/checkout` | Create checkout session |
| POST | `/billing/portal` | Get billing portal URL |
| POST | `/billing/webhook` | Stripe/Razorpay webhook |

#### POST `/billing/checkout`
```json
// Request
{
  "plan": "pro",
  "billing_cycle": "yearly",
  "provider": "stripe"
}

// Response 200
{
  "checkout_url": "https://checkout.stripe.com/...",
  "session_id": "cs_xxx"
}
```

---

## Error Responses

### Standard Error Format
```json
{
  "error": {
    "code": "ACCOUNT_LIMIT_EXCEEDED",
    "message": "Free plan allows only 2 accounts. Upgrade to Pro.",
    "details": {
      "current": 2,
      "limit": 2,
      "upgrade_url": "/billing/checkout?plan=pro"
    }
  }
}
```

### Error Codes
| Code | HTTP | Description |
|------|------|-------------|
| `UNAUTHORIZED` | 401 | Invalid or missing token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `ACCOUNT_LIMIT_EXCEEDED` | 402 | Need to upgrade plan |
| `SYNC_FAILED` | 500 | Account sync error |
| `RATE_LIMITED` | 429 | Too many requests |
| `VALIDATION_ERROR` | 422 | Invalid request body |

---

## Rate Limits

| Plan | Requests/min | Daily Limit |
|------|--------------|-------------|
| Free | 30 | 1,000 |
| Pro | 100 | 10,000 |
| Business | 300 | 50,000 |
| Enterprise | Unlimited | Unlimited |

---

## Webhooks (Outbound)

For Business/Enterprise plans:

```json
POST https://your-server.com/webhook

{
  "event": "transaction.created",
  "timestamp": "2026-01-10T10:00:00Z",
  "data": {
    "transaction_id": "uuid",
    "amount": -4299.00,
    "account_id": "uuid"
  },
  "signature": "sha256=xxx"
}
```

### Event Types
- `transaction.created`
- `account.synced`
- `insight.generated`
- `networth.updated`
- `subscription.changed`
