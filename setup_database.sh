#!/bin/bash

# Database Setup Script for Sprint 1
# This script sets up the database and runs migrations

echo "====================================="
echo "Core Banking API - Database Setup"
echo "====================================="
echo ""

# Step 1: Start Docker services
echo "Step 1: Starting Docker services..."
docker-compose up -d

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Step 2: Create migrations
echo ""
echo "Step 2: Creating migrations for all apps..."
docker-compose exec backend python manage.py makemigrations accounts
docker-compose exec backend python manage.py makemigrations banking
docker-compose exec backend python manage.py makemigrations transactions
docker-compose exec backend python manage.py makemigrations fraud_detection
docker-compose exec backend python manage.py makemigrations audit

# Step 3: Apply migrations
echo ""
echo "Step 3: Applying migrations..."
docker-compose exec backend python manage.py migrate

# Step 4: Create superuser
echo ""
echo "Step 4: Create superuser (admin account)..."
echo "You'll be prompted to enter:"
echo "  - Email: admin@bank.com"
echo "  - Username: admin"
echo "  - Password: (choose a secure password)"
echo ""
docker-compose exec backend python manage.py createsuperuser

echo ""
echo "====================================="
echo "Database setup complete!"
echo "====================================="
echo ""
echo "Next steps:"
echo "1. Access API at: http://localhost:8000/api/"
echo "2. Access Admin panel at: http://localhost:8000/admin/"
echo "3. Access API docs at: http://localhost:8000/api/docs/"
echo ""
echo "To view logs: docker-compose logs -f backend"
echo "To stop services: docker-compose down"
echo ""
