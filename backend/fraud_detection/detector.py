"""
Fraud detection engine.
MVP: Rule-based detection
Future: ML-based anomaly detection using Isolation Forest
"""

from datetime import timedelta
from django.utils import timezone
from django.db.models import Avg, Count
from transactions.models import Transaction


class FraudDetector:
    """
    Rule-based fraud detection system.
    Can be extended with ML models in future sprints.
    """

    def __init__(self, transaction):
        self.transaction = transaction
        self.sender_account = transaction.sender_account
        self.amount = transaction.amount

    def analyze(self):
        """
        Run all fraud detection rules and return results.
        Returns: (is_flagged, fraud_score, reason)
        """
        scores = []
        reasons = []

        # Rule 1: Large transaction amount
        if self.amount > 10000:
            scores.append(0.9)
            reasons.append("Transaction amount exceeds $10,000")

        # Rule 2: Rapid successive transactions
        recent_count = Transaction.objects.filter(
            sender_account=self.sender_account,
            timestamp__gte=timezone.now() - timedelta(minutes=10)
        ).count()

        if recent_count > 5:
            scores.append(0.8)
            reasons.append(f"Multiple transactions in short time ({recent_count} in 10 min)")

        # Rule 3: Unusual amount for user
        avg_transaction = Transaction.objects.filter(
            sender_account=self.sender_account,
            status='completed'
        ).aggregate(Avg('amount'))['amount__avg']

        if avg_transaction and self.amount > (avg_transaction * 5):
            scores.append(0.7)
            reasons.append("Transaction amount 5x higher than user's average")

        # Rule 4: Night-time transaction (elevated risk)
        hour = timezone.now().hour
        if hour < 6 or hour > 22:
            scores.append(0.5)
            reasons.append("Transaction during unusual hours")

        # Calculate final score and flag status
        if scores:
            fraud_score = max(scores)
            is_flagged = fraud_score >= 0.7
            reason = "; ".join(reasons)
        else:
            is_flagged = False
            fraud_score = 0.0
            reason = "No suspicious patterns detected"

        return is_flagged, fraud_score, reason


def detect_fraud(transaction):
    """
    Helper function to detect fraud for a transaction.
    Usage: is_flagged, score, reason = detect_fraud(transaction)
    """
    detector = FraudDetector(transaction)
    return detector.analyze()
