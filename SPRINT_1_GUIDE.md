# Sprint 1 Implementation Guide

**Status**: Ready to Execute
**Estimated Time**: 2-3 hours
**Goal**: Get the Money Transfer API fully working and tested

---

## ✅ What We Just Completed (Phase 1)

All critical code issues have been fixed:

1. ✅ **Email Authentication Backend** - Created [backend/accounts/authentication.py](backend/accounts/authentication.py)
2. ✅ **Django Signals** - Auto-create bank accounts ([backend/banking/signals.py](backend/banking/signals.py))
3. ✅ **Audit Middleware** - Added to settings.py
4. ✅ **Migrations Directories** - Created for all 5 apps
5. ✅ **Test Files** - Added comprehensive tests for all apps
6. ✅ **Setup Scripts** - Created database setup and seeding scripts

---

## 🚀 What You Need to Do Now

### Step 1: Start Docker Desktop

**IMPORTANT**: You need to start Docker Desktop first!

1. Open Docker Desktop application on your Mac
2. Wait for it to say "Docker Desktop is running"
3. Verify it's running:
   ```bash
   docker ps
   ```
   You should see a table (even if empty), not an error.

---

### Step 2: Set Up the Database (Automated)

Once Docker is running, use our automated setup script:

```bash
cd /Users/mrpsycho/Hackathon
chmod +x setup_database.sh
./setup_database.sh
```

This script will:
- Start PostgreSQL database in Docker
- Create all database migrations
- Apply migrations to create tables
- Prompt you to create a superuser

**When prompted for superuser**:
- Email: `admin@bank.com`
- Username: `admin`
- Password: `Admin@1234` (or your choice)

---

### Step 3: Create Test Data

After database setup, create test users and accounts:

```bash
docker-compose exec backend python seed_data.py
```

This creates:
- 1 Admin user
- 1 Auditor user
- 3 Customer users (Alice, Bob, Charlie) with bank accounts and balances

---

### Step 4: Verify API is Running

Check if the API server started:

```bash
docker-compose ps
```

You should see two containers running:
- `hackathon-backend-1` (Django API)
- `hackathon-db-1` (PostgreSQL)

Access the API:
- **API Docs (Swagger)**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/api/health/

---

## 📝 Phase 3: Manual Testing

### Test with curl or Postman

#### 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "Secure@123",
    "password2": "Secure@123",
    "role": "customer"
  }'
```

**Expected**: 201 Created with user details

---

#### 2. Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "Alice@1234"
  }'
```

**Expected**: 200 OK with JWT tokens
**Save the `access` token** - you'll need it for subsequent requests!

---

#### 3. Get Account Details

Replace `YOUR_JWT_TOKEN` with the access token from login:

```bash
curl -X GET http://localhost:8000/api/banking/account/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Expected**: 200 OK with account details and balance

---

#### 4. Transfer Money

Transfer $100 from Alice to Bob:

First, get Bob's account number from seed_data output, then:

```bash
curl -X POST http://localhost:8000/api/transactions/transfer/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_account": "ACC123456789",
    "amount": "100.00",
    "description": "Test transfer"
  }'
```

Replace `ACC123456789` with Bob's actual account number.

**Expected**: 200 OK with transaction details

---

#### 5. View Transaction History

```bash
curl -X GET http://localhost:8000/api/transactions/history/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Expected**: 200 OK with list of transactions

---

#### 6. Test Fraud Detection

Transfer a large amount to trigger fraud detection:

```bash
curl -X POST http://localhost:8000/api/transactions/transfer/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_account": "ACC123456789",
    "amount": "12000.00",
    "description": "Large transfer"
  }'
```

**Expected**: 200 OK but with `"flagged": true`

---

#### 7. View Flagged Transactions (Admin Only)

Login as admin first, get the JWT token, then:

```bash
curl -X GET http://localhost:8000/api/transactions/flagged/ \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN"
```

**Expected**: 200 OK with flagged transactions list

---

#### 8. Test Edge Cases

**Insufficient Balance**:
```bash
curl -X POST http://localhost:8000/api/transactions/transfer/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_account": "ACC123456789",
    "amount": "99999.00",
    "description": "Too much"
  }'
```
**Expected**: 400 Bad Request - "Insufficient balance"

**Transfer to Self**:
```bash
curl -X POST http://localhost:8000/api/transactions/transfer/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_account": "YOUR_OWN_ACCOUNT_NUMBER",
    "amount": "100.00",
    "description": "Self transfer"
  }'
```
**Expected**: 400 Bad Request - "Cannot transfer to your own account"

---

## 🧪 Phase 4: Run Automated Tests

Run the pytest test suite:

```bash
docker-compose exec backend pytest --cov=backend --cov-report=html --cov-report=term-missing
```

**Expected**:
- All tests should pass
- Code coverage should be 70%+ (we're targeting 85%)

View coverage report:
```bash
open backend/htmlcov/index.html
```

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to Docker daemon"
**Solution**: Start Docker Desktop application

### Issue: "Port 8000 already in use"
**Solution**:
```bash
docker-compose down
docker-compose up -d
```

### Issue: "No module named 'accounts'"
**Solution**: Rebuild Docker containers
```bash
docker-compose down
docker-compose up --build
```

### Issue: Migration errors
**Solution**: Reset database (development only!)
```bash
docker-compose down -v
./setup_database.sh
```

### Issue: "Authentication credentials were not provided"
**Solution**: Check that you're passing the JWT token correctly:
```
Authorization: Bearer YOUR_TOKEN_HERE
```
(Note: "Bearer" with capital B, followed by a space)

---

## 📋 Verification Checklist

Before proceeding to create Postman collection:

- [ ] Docker Desktop is running
- [ ] Database migrations completed successfully
- [ ] Superuser created
- [ ] Test data seeded (5 users created)
- [ ] API accessible at http://localhost:8000/api/docs/
- [ ] User registration works
- [ ] User login returns JWT token
- [ ] Get account details works with JWT
- [ ] Money transfer works
- [ ] Transaction history displays
- [ ] Large transfers are flagged
- [ ] Admin can view flagged transactions
- [ ] Insufficient balance is prevented
- [ ] Self-transfer is prevented
- [ ] Tests pass with pytest

---

## 📊 Current Progress

**Sprint 1 Status**: Phase 1 & 2 Complete (Code fixes done, setup scripts ready)

**Remaining**:
- [ ] Start Docker and run setup (YOU DO THIS)
- [ ] Test all endpoints manually
- [ ] Create Postman collection
- [ ] Final testing and bug fixes

---

## 🎯 Next Steps After Manual Testing

Once all manual tests pass:

1. **Create Postman Collection** (I'll help with this)
2. **Run comprehensive tests**
3. **Fix any bugs found**
4. **Prepare for deployment**

---

## 💡 Quick Reference

**Test Credentials** (after running seed_data.py):
```
Admin:   admin@bank.com / Admin@1234
Auditor: auditor@bank.com / Auditor@1234
Alice:   alice@example.com / Alice@1234 (Balance: $10,000)
Bob:     bob@example.com / Bob@1234 (Balance: $5,000)
Charlie: charlie@example.com / Charlie@1234 (Balance: $15,000)
```

**Useful Docker Commands**:
```bash
docker-compose up -d          # Start services
docker-compose down           # Stop services
docker-compose logs -f        # View logs
docker-compose ps             # List containers
docker-compose exec backend bash  # Access backend shell
```

**Useful Django Commands** (inside container):
```bash
docker-compose exec backend python manage.py shell  # Django shell
docker-compose exec backend python manage.py createsuperuser  # Create admin
docker-compose exec backend python manage.py migrate  # Run migrations
```

---

## 🚀 Ready to Continue?

Once you've:
1. Started Docker Desktop
2. Run `./setup_database.sh`
3. Run `docker-compose exec backend python seed_data.py`
4. Verified the API is accessible

Come back and tell me the results! Then we'll create the Postman collection and continue with Sprint 1.

Good luck! 🎉
