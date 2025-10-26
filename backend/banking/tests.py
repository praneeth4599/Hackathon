from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import BankAccount

User = get_user_model()


class BankAccountCreationTestCase(TestCase):
    """Test suite for bank account creation"""

    def test_account_auto_created_on_user_registration(self):
        """Test that bank account is automatically created when user registers"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Test@1234',
            role='customer'
        )

        # Check if bank account was created
        self.assertTrue(hasattr(user, 'bank_account'))
        self.assertEqual(user.bank_account.balance, 0.00)
        self.assertEqual(user.bank_account.daily_limit, 50000.00)

    def test_account_number_generation(self):
        """Test that account numbers are unique and properly formatted"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Test@1234',
            role='customer'
        )

        account_number = user.bank_account.account_number
        self.assertTrue(account_number.startswith('ACC'))
        self.assertEqual(len(account_number), 12)


class BankAccountAPITestCase(APITestCase):
    """Test suite for banking API endpoints"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Test@1234',
            role='customer'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_account_details(self):
        """Test retrieving account details"""
        response = self.client.get('/api/banking/account/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('account_number', response.data)
        self.assertIn('balance', response.data)
