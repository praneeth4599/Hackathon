# Postman API Testing Guide

This directory contains Postman collections for testing the Core Banking API.

## 📦 What's Inside

- `banking-api.postman_collection.json` - Complete API test collection (to be created in Sprint 1)
- `banking-api.postman_environment.json` - Environment variables for local and production testing

## 🚀 Quick Start

### 1. Import Collection into Postman

1. Open Postman
2. Click **Import** button (top left)
3. Select `banking-api.postman_collection.json`
4. Collection will appear in the left sidebar

### 2. Setup Environment Variables

**Local Development:**
```json
{
  "name": "Local",
  "values": [
    {
      "key": "base_url",
      "value": "http://localhost:8000",
      "enabled": true
    },
    {
      "key": "jwt_token",
      "value": "",
      "enabled": true
    }
  ]
}
```

**Production (Render/Vercel):**
```json
{
  "name": "Production",
  "values": [
    {
      "key": "base_url",
      "value": "https://your-banking-api.onrender.com",
      "enabled": true
    },
    {
      "key": "jwt_token",
      "value": "",
      "enabled": true
    }
  ]
}
```

### 3. Run the Collection

#### Option A: Manual Testing
1. Select environment from dropdown (top right)
2. Expand collection in sidebar
3. Click on individual requests
4. Click **Send** button
5. View response

#### Option B: Automated Testing (Collection Runner)
1. Click on collection name
2. Click **Run** button
3. Select environment
4. Click **Run Banking API**
5. View test results

## 📋 API Endpoints Included

### Authentication
- ✅ `POST /api/auth/register/` - Register new user
- ✅ `POST /api/auth/login/` - Login and get JWT token
- ✅ `POST /api/auth/token/refresh/` - Refresh expired token

### Transactions
- ✅ `POST /api/transactions/transfer/` - Transfer money
- ✅ `GET /api/transactions/history/` - Get transaction history
- ✅ `GET /api/transactions/{id}/` - Get transaction details

### Admin (Requires admin role)
- ✅ `GET /api/admin/flagged-transactions/` - View flagged transactions
- ✅ `GET /api/audit/logs/` - View audit logs

## 🧪 Test Scenarios Covered

### 1. Authentication Flow
- Register new customer
- Login with valid credentials
- Login with invalid credentials (should fail)
- Access protected endpoint without token (should fail)
- Refresh JWT token

### 2. Money Transfer - Success Cases
- Transfer with sufficient balance
- Verify sender balance deducted
- Verify receiver balance increased

### 3. Money Transfer - Validation
- Insufficient balance → 400 error
- Invalid receiver account → 404 error
- Negative amount → 400 error
- Transfer to same account → 400 error
- Daily limit exceeded → 429 error

### 4. Security Tests
- Transfer without JWT → 401 error
- Transfer with expired token → 401 error
- Customer accessing admin endpoint → 403 error
- Rate limiting (11 rapid requests) → 429 error

### 5. Fraud Detection
- Large transfer (>$10,000) gets flagged
- Multiple rapid transfers get flagged

## 🔧 Automated Test Scripts

The collection includes automated test scripts that:

### Pre-request Scripts
```javascript
// Auto-attach JWT token to requests
if (pm.environment.get("jwt_token")) {
    pm.request.headers.add({
        key: 'Authorization',
        value: 'Bearer ' + pm.environment.get('jwt_token')
    });
}
```

### Test Scripts (Assertions)
```javascript
// Login endpoint - save token
pm.test("Login successful", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.environment.set("jwt_token", jsonData.access);
    pm.environment.set("refresh_token", jsonData.refresh);
});

// Transfer endpoint - validate response
pm.test("Transfer completed", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData.status).to.eql("success");
    pm.expect(jsonData.transaction_id).to.not.be.empty;
});

// Error handling - validate error responses
pm.test("Insufficient balance error", function () {
    pm.response.to.have.status(400);
    var jsonData = pm.response.json();
    pm.expect(jsonData.error).to.include("insufficient");
});
```

## 📊 Expected Test Results

When running the full collection, you should see:

```
Total Tests: 25
Passed: 25
Failed: 0
Skipped: 0
```

### Test Breakdown:
- Authentication: 5/5 passed
- Transfer Success: 3/3 passed
- Transfer Validation: 6/6 passed
- Security: 4/4 passed
- Fraud Detection: 2/2 passed
- Admin Endpoints: 5/5 passed

## 🎯 Demo Flow

For hackathon demo, follow this sequence:

1. **Setup** (30 seconds)
   - Select "Production" environment
   - Show environment variables

2. **Authentication** (1 minute)
   - Run: Register new user → 201 Created
   - Run: Login → 200 OK
   - Show JWT token saved in environment

3. **Happy Path** (1 minute)
   - Run: Transfer $1000 → 200 OK
   - Show transaction_id and new balance
   - Run: Get history → Show transaction listed

4. **Edge Cases** (1 minute)
   - Run: Transfer $999,999 → 400 Insufficient Funds
   - Run: Transfer to invalid account → 404 Not Found
   - Run: Transfer $-100 → 400 Invalid Amount

5. **Security** (1 minute)
   - Remove JWT token from environment
   - Run: Transfer → 401 Unauthorized
   - Add token back
   - Run: Transfer 11 times → 429 Rate Limit

6. **Fraud Detection** (30 seconds)
   - Run: Transfer $15,000 → 200 OK but flagged=true
   - Login as admin
   - Run: Get flagged transactions → Shows the $15K transfer

## 🔍 Debugging Tips

### Common Issues

**Issue**: 401 Unauthorized
```
Solution:
1. Check if jwt_token is set in environment
2. Token may have expired - run Login again
3. Verify Authorization header format: "Bearer <token>"
```

**Issue**: 404 Not Found
```
Solution:
1. Check base_url is correct
2. Verify API is running (local: http://localhost:8000)
3. Check endpoint spelling
```

**Issue**: CORS errors
```
Solution:
1. Ensure Django CORS settings include your domain
2. Check CORS_ALLOWED_ORIGINS in settings.py
```

**Issue**: Connection refused
```
Solution:
1. Start backend server: docker-compose up
2. Check if port 8000 is available
3. Verify database is running
```

## 📝 Creating the Collection (Sprint 1)

During Sprint 1, you'll create the actual collection file. Here's the structure:

```json
{
  "info": {
    "name": "Core Banking API",
    "description": "Money Transfer System with Security & Fraud Detection",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "Register",
          "request": {
            "method": "POST",
            "header": [],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"username\": \"test_user\",\n  \"email\": \"test@example.com\",\n  \"password\": \"Secure@123\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            },
            "url": {
              "raw": "{{base_url}}/api/auth/register/",
              "host": ["{{base_url}}"],
              "path": ["api", "auth", "register", ""]
            }
          }
        }
      ]
    }
  ]
}
```

## 🎓 Learning Resources

- [Postman Documentation](https://learning.postman.com/docs/)
- [Writing Tests in Postman](https://learning.postman.com/docs/writing-scripts/test-scripts/)
- [Environment Variables](https://learning.postman.com/docs/sending-requests/managing-environments/)
- [Collection Runner](https://learning.postman.com/docs/running-collections/intro-to-collection-runs/)

## ✅ Checklist for Sprint 1

- [ ] Create `banking-api.postman_collection.json`
- [ ] Create `banking-api.postman_environment.json`
- [ ] Add all authentication endpoints
- [ ] Add all transaction endpoints
- [ ] Add all admin endpoints
- [ ] Write test scripts for each request
- [ ] Test locally
- [ ] Test on production deployment
- [ ] Export and commit to git

---

**Note**: The actual collection files will be created during Sprint 1 implementation. This README serves as a guide for how to use them once created.
