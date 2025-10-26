from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from banking.models import BankAccount
from .models import Transaction
from decimal import Decimal

User = get_user_model()


class MoneyTransferTestCase(APITestCase):
    """Test suite for money transfer functionality"""

    def setUp(self):
        # Create sender
        self.sender = User.objects.create_user(
            username='sender',
            email='sender@example.com',
            password='Test@1234',
            role='customer'
        )
        self.sender.bank_account.balance = Decimal('1000.00')
        self.sender.bank_account.save()

        # Create receiver
        self.receiver = User.objects.create_user(
            username='receiver',
            email='receiver@example.com',
            password='Test@1234',
            role='customer'
        )
        self.receiver.bank_account.balance = Decimal('500.00')
        self.receiver.bank_account.save()

        self.client.force_authenticate(user=self.sender)

    def test_successful_transfer(self):
        """Test successful money transfer"""
        payload = {
            'receiver_account': self.receiver.bank_account.account_number,
            'amount': '100.00',
            'description': 'Test transfer'
        }

        response = self.client.post('/api/transactions/transfer/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')

        # Verify balances
        self.sender.bank_account.refresh_from_db()
        self.receiver.bank_account.refresh_from_db()
        self.assertEqual(self.sender.bank_account.balance, Decimal('900.00'))
        self.assertEqual(self.receiver.bank_account.balance, Decimal('600.00'))

    def test_insufficient_balance(self):
        """Test transfer fails with insufficient balance"""
        payload = {
            'receiver_account': self.receiver.bank_account.account_number,
            'amount': '2000.00',
            'description': 'Test transfer'
        }

        response = self.client.post('/api/transactions/transfer/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Insufficient balance', response.data['error'])

    def test_negative_amount(self):
        """Test transfer fails with negative amount"""
        payload = {
            'receiver_account': self.receiver.bank_account.account_number,
            'amount': '-100.00',
            'description': 'Test transfer'
        }

        response = self.client.post('/api/transactions/transfer/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transfer_to_same_account(self):
        """Test transfer to same account is prevented"""
        payload = {
            'receiver_account': self.sender.bank_account.account_number,
            'amount': '100.00',
            'description': 'Test transfer'
        }

        response = self.client.post('/api/transactions/transfer/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cannot transfer to your own account', response.data['error'])

    def test_large_transaction_flagged(self):
        """Test that large transactions are flagged"""
        self.sender.bank_account.balance = Decimal('15000.00')
        self.sender.bank_account.save()

        payload = {
            'receiver_account': self.receiver.bank_account.account_number,
            'amount': '12000.00',
            'description': 'Large transfer'
        }

        response = self.client.post('/api/transactions/transfer/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['flagged'])
