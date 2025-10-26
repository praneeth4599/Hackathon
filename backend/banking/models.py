from django.db import models
from django.conf import settings
import random
import string


class BankAccount(models.Model):
    """
    Bank Account model for managing customer accounts.
    Automatically creates account when user registers.
    """
    ACCOUNT_TYPE_CHOICES = [
        ('savings', 'Savings Account'),
        ('current', 'Current Account'),
        ('fd', 'Fixed Deposit'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bank_account'
    )
    account_number = models.CharField(max_length=12, unique=True, editable=False)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='savings')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    daily_limit = models.DecimalField(max_digits=10, decimal_places=2, default=50000.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bank_accounts'
        verbose_name = 'Bank Account'
        verbose_name_plural = 'Bank Accounts'

    def __str__(self):
        return f"{self.account_number} - {self.user.email} (Balance: ${self.balance})"

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_account_number():
        """Generate unique 12-digit account number starting with ACC"""
        while True:
            number = 'ACC' + ''.join(random.choices(string.digits, k=9))
            if not BankAccount.objects.filter(account_number=number).exists():
                return number
