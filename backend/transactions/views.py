from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction as db_transaction
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import Transaction
from banking.models import BankAccount
from .serializers import TransferSerializer, TransactionSerializer


class TransferMoneyView(generics.CreateAPIView):
    """
    Money transfer endpoint with validation, fraud detection, and rate limiting.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TransferSerializer

    @method_decorator(ratelimit(key='user', rate='10/m', method='POST'))
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver_account_number = serializer.validated_data['receiver_account']
        amount = serializer.validated_data['amount']
        description = serializer.validated_data.get('description', '')

        # Get sender's account
        try:
            sender_account = request.user.bank_account
        except BankAccount.DoesNotExist:
            return Response(
                {'error': 'You do not have a bank account'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get receiver's account
        receiver_account = BankAccount.objects.get(account_number=receiver_account_number)

        # Validation: Cannot transfer to same account
        if sender_account == receiver_account:
            return Response(
                {'error': 'Cannot transfer to your own account'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validation: Insufficient balance
        if sender_account.balance < amount:
            return Response(
                {'error': 'Insufficient balance'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validation: Daily limit check
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_transfers = Transaction.objects.filter(
            sender_account=sender_account,
            timestamp__gte=today_start,
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0

        if today_transfers + amount > sender_account.daily_limit:
            return Response(
                {'error': 'Daily transfer limit exceeded'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Fraud detection (simple rule-based for MVP)
        flagged = False
        fraud_score = 0.0
        fraud_reason = None

        # Rule 1: Large transaction
        if amount > 10000:
            flagged = True
            fraud_score = 0.9
            fraud_reason = "Large transaction amount"

        # Rule 2: Rapid transactions
        recent_count = Transaction.objects.filter(
            sender_account=sender_account,
            timestamp__gte=timezone.now() - timedelta(minutes=10)
        ).count()

        if recent_count > 5:
            flagged = True
            fraud_score = max(fraud_score, 0.8)
            fraud_reason = "Multiple rapid transactions"

        # Atomic transaction execution
        try:
            with db_transaction.atomic():
                # Deduct from sender
                sender_account.balance -= amount
                sender_account.save()

                # Add to receiver
                receiver_account.balance += amount
                receiver_account.save()

                # Create transaction record
                transaction_obj = Transaction.objects.create(
                    sender_account=sender_account,
                    receiver_account=receiver_account,
                    amount=amount,
                    description=description,
                    status='completed',
                    flagged=flagged,
                    fraud_score=fraud_score,
                    fraud_reason=fraud_reason
                )

                return Response({
                    'transaction_id': transaction_obj.transaction_id,
                    'status': 'success',
                    'amount': str(amount),
                    'sender_account': sender_account.account_number,
                    'receiver_account': receiver_account.account_number,
                    'sender_new_balance': str(sender_account.balance),
                    'timestamp': transaction_obj.timestamp,
                    'flagged': flagged,
                    'fraud_score': str(fraud_score) if fraud_score > 0 else None
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Transaction failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TransactionHistoryView(generics.ListAPIView):
    """Get transaction history for authenticated user"""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_account = self.request.user.bank_account
        return Transaction.objects.filter(
            Q(sender_account=user_account) | Q(receiver_account=user_account)
        ).order_by('-timestamp')


class FlaggedTransactionsView(generics.ListAPIView):
    """Admin endpoint to view flagged transactions"""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow admins and auditors
        if self.request.user.role not in ['admin', 'auditor']:
            return Transaction.objects.none()

        return Transaction.objects.filter(flagged=True).order_by('-timestamp')
