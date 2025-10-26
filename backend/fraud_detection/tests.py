from django.test import TestCase
from django.contrib.auth import get_user_model
from banking.models import BankAccount
from transactions.models import Transaction
from .detector import FraudDetector
from decimal import Decimal

User = get_user_model()


class FraudDetectionTestCase(TestCase):
    """Test suite for fraud detection"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Test@1234',
            role='customer'
        )
        self.user.bank_account.balance = Decimal('20000.00')
        self.user.bank_account.save()

        self.receiver = User.objects.create_user(
            username='receiver',
            email='receiver@example.com',
            password='Test@1234',
            role='customer'
        )

    def test_large_transaction_detected(self):
        """Test that large transactions are flagged"""
        transaction = Transaction(
            sender_account=self.user.bank_account,
            receiver_account=self.receiver.bank_account,
            amount=Decimal('15000.00')
        )

        detector = FraudDetector(transaction)
        is_flagged, fraud_score, reason = detector.analyze()

        self.assertTrue(is_flagged)
        self.assertGreaterEqual(fraud_score, 0.7)
        self.assertIn('10,000', reason)

    def test_normal_transaction_not_flagged(self):
        """Test that normal transactions are not flagged"""
        transaction = Transaction(
            sender_account=self.user.bank_account,
            receiver_account=self.receiver.bank_account,
            amount=Decimal('500.00')
        )

        detector = FraudDetector(transaction)
        is_flagged, fraud_score, reason = detector.analyze()

        self.assertFalse(is_flagged)
