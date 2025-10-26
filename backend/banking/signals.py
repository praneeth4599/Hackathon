"""
Django signals for banking app.
Auto-creates a bank account when a new user is registered.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import BankAccount


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_bank_account(sender, instance, created, **kwargs):
    """
    Automatically create a bank account when a new user is created.
    Only creates for customer role users.
    """
    if created and instance.role == 'customer':
        BankAccount.objects.create(
            user=instance,
            account_type='savings',
            balance=0.00,
            daily_limit=50000.00
        )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_bank_account(sender, instance, **kwargs):
    """
    Save the bank account when user is saved.
    This ensures the account is always synced with the user.
    """
    if hasattr(instance, 'bank_account'):
        instance.bank_account.save()
