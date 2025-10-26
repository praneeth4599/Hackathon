"""
Test Data Seeding Script
Creates sample users and bank accounts for testing
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from accounts.models import User
from banking.models import BankAccount
from decimal import Decimal


def create_test_data():
    print("=" * 50)
    print("Creating test data for Core Banking API")
    print("=" * 50)
    print()

    # Create Admin User
    print("1. Creating Admin user...")
    admin, created = User.objects.get_or_create(
        email='admin@bank.com',
        defaults={
            'username': 'admin',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('Admin@1234')
        admin.save()
        print(f"   ✓ Admin created: {admin.email}")
    else:
        print(f"   → Admin already exists: {admin.email}")

    # Create Auditor User
    print("\n2. Creating Auditor user...")
    auditor, created = User.objects.get_or_create(
        email='auditor@bank.com',
        defaults={
            'username': 'auditor',
            'role': 'auditor',
            'is_staff': True
        }
    )
    if created:
        auditor.set_password('Auditor@1234')
        auditor.save()
        print(f"   ✓ Auditor created: {auditor.email}")
    else:
        print(f"   → Auditor already exists: {auditor.email}")

    # Create Customer 1 - Alice
    print("\n3. Creating Customer 1 (Alice)...")
    alice, created = User.objects.get_or_create(
        email='alice@example.com',
        defaults={
            'username': 'alice',
            'role': 'customer',
            'phone_number': '+1234567890'
        }
    )
    if created:
        alice.set_password('Alice@1234')
        alice.save()
        # Bank account will be auto-created by signal
        alice.bank_account.balance = Decimal('10000.00')
        alice.bank_account.save()
        print(f"   ✓ Customer created: {alice.email}")
        print(f"   ✓ Account Number: {alice.bank_account.account_number}")
        print(f"   ✓ Initial Balance: ${alice.bank_account.balance}")
    else:
        print(f"   → Customer already exists: {alice.email}")
        print(f"   → Account Number: {alice.bank_account.account_number}")

    # Create Customer 2 - Bob
    print("\n4. Creating Customer 2 (Bob)...")
    bob, created = User.objects.get_or_create(
        email='bob@example.com',
        defaults={
            'username': 'bob',
            'role': 'customer',
            'phone_number': '+1234567891'
        }
    )
    if created:
        bob.set_password('Bob@1234')
        bob.save()
        # Bank account will be auto-created by signal
        bob.bank_account.balance = Decimal('5000.00')
        bob.bank_account.save()
        print(f"   ✓ Customer created: {bob.email}")
        print(f"   ✓ Account Number: {bob.bank_account.account_number}")
        print(f"   ✓ Initial Balance: ${bob.bank_account.balance}")
    else:
        print(f"   → Customer already exists: {bob.email}")
        print(f"   → Account Number: {bob.bank_account.account_number}")

    # Create Customer 3 - Charlie
    print("\n5. Creating Customer 3 (Charlie)...")
    charlie, created = User.objects.get_or_create(
        email='charlie@example.com',
        defaults={
            'username': 'charlie',
            'role': 'customer',
            'phone_number': '+1234567892'
        }
    )
    if created:
        charlie.set_password('Charlie@1234')
        charlie.save()
        # Bank account will be auto-created by signal
        charlie.bank_account.balance = Decimal('15000.00')
        charlie.bank_account.save()
        print(f"   ✓ Customer created: {charlie.email}")
        print(f"   ✓ Account Number: {charlie.bank_account.account_number}")
        print(f"   ✓ Initial Balance: ${charlie.bank_account.balance}")
    else:
        print(f"   → Customer already exists: {charlie.email}")
        print(f"   → Account Number: {charlie.bank_account.account_number}")

    print("\n" + "=" * 50)
    print("Test Data Created Successfully!")
    print("=" * 50)
    print("\nTest Credentials:")
    print("-" * 50)
    print("Admin:   admin@bank.com / Admin@1234")
    print("Auditor: auditor@bank.com / Auditor@1234")
    print("Alice:   alice@example.com / Alice@1234")
    print("Bob:     bob@example.com / Bob@1234")
    print("Charlie: charlie@example.com / Charlie@1234")
    print("-" * 50)
    print("\nAccount Numbers:")
    print("-" * 50)

    customers = [alice, bob, charlie]
    for user in customers:
        if hasattr(user, 'bank_account'):
            print(f"{user.username.capitalize():8} {user.bank_account.account_number}  (Balance: ${user.bank_account.balance})")

    print("-" * 50)
    print()


if __name__ == '__main__':
    create_test_data()
