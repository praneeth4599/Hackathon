# Core Banking System - Money Transfer API

A secure banking backend system focused on money transfer functionality with fraud detection, audit logging, and role-based access control.

## Problem Statement

This project implements a core banking backend system that handles:
- User authentication and authorization
- Secure money transfers between accounts
- Fraud detection for suspicious transactions
- Comprehensive audit logging
- Role-based access control for different user types

**Implementation Focus**: Money Transfer (Use Case 3 from the problem statement)

## Why Money Transfer?

After analyzing all the use cases, I chose to implement the money transfer feature because:

**Business Value**: It's the most frequently used feature in any banking system. Every customer needs to transfer money, making it essential for demonstrating core functionality.

**Security Coverage**: This single use case naturally incorporates all five required security features:
- JWT authentication for every transfer request
- Password hashing for user credential protection
- Rate limiting to prevent abuse
- Role-based access control (customers can transfer, admins can review)
- Input validation to prevent malicious data

**Testing Depth**: Money transfers provide excellent testing scenarios - successful transfers, insufficient balance, invalid accounts, fraud detection, and security validations.

**Technical Complexity**: It demonstrates ACID transactions, concurrent access handling, and real-time balance management - all critical for backend systems.

## System Architecture

```
Client (Postman/API Consumer)
           |
           | HTTPS + JWT Token
           v
    Django REST API
           |
           |-- Authentication Layer (JWT)
           |-- Rate Limiting
           |-- Business Logic (Transfer Validation)
           |-- Fraud Detection
           |-- Audit Logging
           |
           v
    PostgreSQL Database
```

## Live Demo

- API Base URL: `https://your-banking-api.onrender.com` (will be updated after deployment)
- Postman Collection: Available in `/postman` directory
- API Documentation: `/api/docs/` (Swagger UI)

Test Accounts:
```
Customer: customer@bank.com / Test@1234
Admin: admin@bank.com / Admin@1234
```

## Use Case Flow: Money Transfer

**Actors**: Customer (initiates transfer), Bank Admin (reviews flagged items), Auditor (monitors logs)

**Flow**:
1. Customer logs in and receives JWT token
2. Customer submits transfer request with receiver account and amount
3. System validates JWT token
4. System checks sender balance and daily limit
5. Fraud detection analyzes transaction pattern
6. If valid, system executes atomic transaction (deduct from sender, add to receiver)
7. Audit log created with transaction details
8. Response sent with transaction ID and updated balance

**Edge Cases Handled**:

| Scenario | HTTP Response | Status Code |
|----------|--------------|-------------|
| Successful transfer | Transaction completed | 200 OK |
| Insufficient balance | Error message | 400 Bad Request |
| Daily limit exceeded | Limit reached message | 429 Too Many Requests |
| Invalid receiver account | Account not found | 404 Not Found |
| Transfer to same account | Invalid operation | 400 Bad Request |
| Negative amount | Invalid amount | 400 Bad Request |
| No authentication | Auth required | 401 Unauthorized |
| Wrong permissions | Access denied | 403 Forbidden |
| Suspicious pattern | Transaction flagged but completed | 200 OK |

## API Endpoints

### Authentication

**Register User**
```
POST /api/auth/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "Secure@123",
  "role": "customer"
}

Response (201 Created):
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "role": "customer",
  "account_number": "ACC1234567890"
}
```

**Login**
```
POST /api/auth/login/
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "Secure@123"
}

Response (200 OK):
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "role": "customer"
  }
}
```

### Transactions (Requires Authentication)

**Transfer Money**
```
POST /api/transactions/transfer/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "receiver_account": "ACC9876543210",
  "amount": 1500.00,
  "description": "Payment for services"
}

Response (200 OK):
{
  "transaction_id": "TXN202510260001",
  "status": "success",
  "amount": 1500.00,
  "sender_account": "ACC1234567890",
  "receiver_account": "ACC9876543210",
  "sender_new_balance": 3500.00,
  "timestamp": "2025-10-26T10:30:00Z",
  "flagged": false
}
```

**Get Transaction History**
```
GET /api/transactions/history/?limit=10&offset=0
Authorization: Bearer <jwt_token>

Response (200 OK):
{
  "count": 25,
  "next": "http://api/transactions/history/?limit=10&offset=10",
  "previous": null,
  "results": [
    {
      "transaction_id": "TXN202510260001",
      "type": "debit",
      "amount": 1500.00,
      "other_account": "ACC9876543210",
      "balance_after": 3500.00,
      "timestamp": "2025-10-26T10:30:00Z"
    }
  ]
}
```

### Admin Endpoints (Admin Role Required)

**View Flagged Transactions**
```
GET /api/admin/flagged-transactions/
Authorization: Bearer <admin_jwt_token>

Response (200 OK):
{
  "results": [
    {
      "transaction_id": "TXN202510260050",
      "amount": 15000.00,
      "sender": "ACC1234567890",
      "receiver": "ACC9999999999",
      "fraud_score": 0.85,
      "reason": "Anomalously large transfer",
      "timestamp": "2025-10-26T14:20:00Z"
    }
  ]
}
```

**Get Audit Logs**
```
GET /api/audit/logs/?user_id=1&action=transfer
Authorization: Bearer <admin_jwt_token>
```

## Security Features

### 1. JWT-Based Authentication
Using `djangorestframework-simplejwt` for token-based authentication.
- Access tokens expire after 1 hour
- Refresh tokens valid for 7 days
- HS256 algorithm for signing
- Required for all transaction and user-specific endpoints

### 2. Password Hashing
Using Django's built-in BCrypt password hasher for secure credential storage.

Password requirements:
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 number
- At least 1 special character

### 3. Rate Limiting
Implemented using `django-ratelimit` to prevent abuse:
- Login endpoint: 5 requests per minute
- Transfer endpoint: 10 requests per minute
- Registration: 3 requests per minute

### 4. Role-Based Access Control (RBAC)

Three user roles with different permissions:

| Role | Permissions |
|------|-------------|
| Customer | Transfer money, view own transactions and account |
| Admin | View all transactions, review flagged items, manage user accounts |
| Auditor | Read-only access to audit logs and all transactions |

### 5. Input Validation & Sanitization
- Django REST Framework serializers for type validation
- Custom validators for account numbers and amounts
- SQL injection prevention through Django ORM
- HTML tag stripping and special character escaping

## Testing Strategy

### Unit Tests (pytest)
Target coverage: 85%+

```bash
# Run tests
pytest --cov=. --cov-report=html
```

Test files will cover:
- Balance validation logic
- Daily limit enforcement
- Fraud detection algorithm
- Account existence checks
- Authentication and authorization

### API Integration Tests (Postman)

The Postman collection includes test suites for:

1. Authentication Flow (5 tests)
   - User registration
   - Valid and invalid login attempts
   - Token refresh
   - Unauthorized access attempts

2. Transfer Success Cases (3 tests)
   - Valid transfer execution
   - Balance verification
   - Transaction history update

3. Validation Tests (6 tests)
   - Insufficient balance handling
   - Invalid account numbers
   - Negative amounts
   - Self-transfers
   - Daily limit checks
   - Maximum amount validation

4. Security Tests (4 tests)
   - Missing JWT tokens
   - Expired tokens
   - Unauthorized role access
   - Rate limiting enforcement

5. Fraud Detection (2 tests)
   - Large transaction flagging
   - Rapid transaction detection

See `/postman/README.md` for detailed testing guide.

## Deployment

### Platform: Render + Supabase

**Render** for backend hosting (free tier)
**Supabase** for PostgreSQL database (free tier)

Benefits:
- Free hosting with automatic HTTPS
- Managed PostgreSQL database with connection pooling
- Automatic deployments from GitHub
- Built-in environment variable management

### Deployment Steps

**Step 1: Set up Supabase Database**

1. Go to [supabase.com](https://supabase.com) and create account
2. Create new project
3. Go to Project Settings → Database
4. Copy the connection string (it looks like):
   ```
   postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```
5. Save this connection string - you'll need it for Render

**Step 2: Prepare Your Repository**

1. Ensure all code is committed to GitHub:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. Your repository should have:
   - `render.yaml` (already configured)
   - `build.sh` (deployment script)
   - `requirements.txt` (all dependencies)
   - `.env.example` (template for environment variables)

**Step 3: Deploy to Render**

1. Go to [render.com](https://render.com) and create account
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Render will auto-detect the `render.yaml` file
5. Configure environment variables:

   **Required Environment Variables:**
   ```
   DATABASE_URL = postgresql://postgres:[YOUR_PASSWORD]@db.lkoiyvnkuaaxpcuimvbw.supabase.co:5432/postgres
   SECRET_KEY = (auto-generated by Render)
   DEBUG = False
   ALLOWED_HOSTS = your-app-name.onrender.com
   ```

6. Click **"Create Web Service"**
7. Render will automatically:
   - Install dependencies
   - Run migrations on Supabase database
   - Collect static files
   - Start the server with gunicorn

**Step 4: Create Admin User on Production**

1. Once deployed, go to your Render dashboard
2. Click on your web service → **"Shell"**
3. Run:
   ```bash
   cd backend
   python manage.py createsuperuser
   ```
4. Enter admin credentials

**Step 5: Test Your Live API**

Your API will be available at: `https://your-app-name.onrender.com`

Test endpoints:
```bash
# Login
curl -X POST https://your-app-name.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@bank.com","password":"YourAdminPassword"}'

# View API docs
https://your-app-name.onrender.com/api/docs/
```

**Configuration Files:**

The `render.yaml` is already configured:
```yaml
services:
  - type: web
    name: banking-api
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt && cd backend && python manage.py collectstatic --no-input && python manage.py migrate"
    startCommand: "cd backend && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT"
    envVars:
      - key: DATABASE_URL
        sync: false  # You'll set this manually with your Supabase URL
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
```

**Troubleshooting:**

If deployment fails, check Render logs:
- Build logs: Check for dependency installation errors
- Deploy logs: Check for migration errors
- Runtime logs: Check for database connection issues

Common issues:
- **Database connection error**: Verify DATABASE_URL is correct
- **Static files not loading**: Check ALLOWED_HOSTS includes your Render domain
- **Migration errors**: Run migrations manually via Render shell

## Database Schema

### Users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) DEFAULT 'customer',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Bank Accounts
```sql
CREATE TABLE bank_accounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    account_number VARCHAR(12) UNIQUE NOT NULL,
    account_type VARCHAR(20),
    balance DECIMAL(15, 2) DEFAULT 0.00,
    daily_limit DECIMAL(10, 2) DEFAULT 50000.00,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Transactions
```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(20) UNIQUE NOT NULL,
    sender_account_id INTEGER REFERENCES bank_accounts(id),
    receiver_account_id INTEGER REFERENCES bank_accounts(id),
    amount DECIMAL(15, 2) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'completed',
    flagged BOOLEAN DEFAULT FALSE,
    fraud_score DECIMAL(3, 2),
    timestamp TIMESTAMP DEFAULT NOW()
);
```

### Audit Logs
```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(50) NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    details JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | Django | 3.2.25 |
| API | Django REST Framework | 3.15.1 |
| Database | PostgreSQL | 13+ |
| Authentication | djangorestframework-simplejwt | 5.2.2 |
| Rate Limiting | django-ratelimit | 4.1.0 |
| ML | scikit-learn | 1.3.0 |
| Testing | pytest-django | 4.5.2 |
| Server | Gunicorn | 20.1.0 |
| Static Files | WhiteNoise | 6.2.0 |
| Containerization | Docker | Latest |

## Project Structure

```
Hackathon/
├── backend/
│   ├── backend/              # Django settings and configuration
│   ├── accounts/             # User management and authentication
│   ├── banking/              # Bank account models and views
│   ├── transactions/         # Money transfer logic
│   ├── fraud_detection/      # Anomaly detection
│   ├── audit/                # Audit logging
│   └── manage.py
├── postman/
│   ├── banking-api.postman_collection.json
│   └── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Local Development Setup

### Using Docker (Recommended)

```bash
# Clone repository
git clone <repo-url>
cd Hackathon

# Create environment file
cp .env.example .env

# Start services
docker-compose up --build

# Create superuser (in new terminal)
docker-compose exec backend python manage.py createsuperuser

# Access API at http://localhost:8000/api/
```

### Manual Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
cd backend
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

## Fraud Detection

### Rule-Based Approach (MVP)
```python
def is_suspicious(transaction):
    # Flag large transactions
    if transaction.amount > 10000:
        return True, 0.9

    # Flag rapid transfers
    recent_count = Transaction.objects.filter(
        sender=transaction.sender,
        timestamp__gte=timezone.now() - timedelta(minutes=10)
    ).count()

    if recent_count > 5:
        return True, 0.8

    return False, 0.0
```

### ML-Based (Optional Enhancement)
Using scikit-learn's Isolation Forest algorithm to detect anomalies based on:
- Transaction amount
- Time of day
- Transaction frequency
- Average transaction size for user
- Time since last transaction

## Demo Script

For the hackathon presentation:

1. **Introduction** (30 seconds)
   - Explain why money transfer was chosen
   - Highlight security features

2. **Live Demo with Postman** (3 minutes)
   - Register and login to get JWT
   - Execute successful transfer
   - Demonstrate validation (insufficient balance)
   - Show rate limiting in action
   - Trigger fraud detection with large amount
   - Admin view of flagged transaction

3. **Architecture Overview** (1 minute)
   - Explain PostgreSQL transactions for atomicity
   - JWT for stateless authentication
   - Fraud detection integration

4. **Q&A** (30 seconds)

## Common Issues

**Database Connection Error**
```bash
# Check if PostgreSQL is running
docker ps

# Verify environment variables
cat .env
```

**JWT Token Expired**
```bash
# Use refresh endpoint
POST /api/auth/token/refresh/
{
  "refresh": "<refresh_token>"
}
```

**Migration Conflicts**
```bash
# Reset database (development only)
docker-compose down -v
docker-compose up --build
python manage.py migrate
```

## Future Enhancements

- Scheduled transfers using Celery
- Loan application workflow
- Enhanced ML fraud detection
- Real-time notifications via WebSockets
- Multi-currency support
- Two-factor authentication
- PDF statement generation

## Team

Developer: [Your Name]
Hackathon: [Event Name]
Date: October 2025

## License

Built for hackathon and educational purposes.
