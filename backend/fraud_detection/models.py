from django.db import models
from transactions.models import Transaction


class FraudAlert(models.Model):
    """
    Model to track fraud alerts for suspicious transactions.
    Used for admin review and ML training.
    """
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('investigating', 'Under Investigation'),
        ('confirmed', 'Confirmed Fraud'),
        ('false_positive', 'False Positive'),
    ]

    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name='fraud_alert'
    )
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    detection_reason = models.TextField()
    fraud_score = models.DecimalField(max_digits=3, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_fraud_alerts'
    )
    review_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'fraud_alerts'
        verbose_name = 'Fraud Alert'
        verbose_name_plural = 'Fraud Alerts'
        ordering = ['-created_at']

    def __str__(self):
        return f"Alert {self.id} - {self.transaction.transaction_id} ({self.severity})"
