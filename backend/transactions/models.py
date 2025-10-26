from django.db import models
from banking.models import BankAccount
from django.utils import timezone
import random
import string


class Transaction(models.Model):
    """
    Transaction model for money transfers.
    Implements atomic transfer logic with fraud detection.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('flagged', 'Flagged'),
    ]

    transaction_id = models.CharField(max_length=20, unique=True, editable=False)
    sender_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name='sent_transactions'
    )
    receiver_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name='received_transactions'
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    flagged = models.BooleanField(default=False)
    fraud_score = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    fraud_reason = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.transaction_id} - ${self.amount} ({self.sender_account.account_number} → {self.receiver_account.account_number})"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_transaction_id():
        """Generate unique transaction ID with format TXN{timestamp}{random}"""
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_suffix = ''.join(random.choices(string.digits, k=4))
        return f"TXN{timestamp}{random_suffix}"
