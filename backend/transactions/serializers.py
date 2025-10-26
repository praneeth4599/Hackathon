from rest_framework import serializers
from .models import Transaction
from banking.models import BankAccount


class TransferSerializer(serializers.Serializer):
    receiver_account = serializers.CharField(max_length=12)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        if value > 1000000:
            raise serializers.ValidationError("Amount exceeds maximum transfer limit")
        return value

    def validate_receiver_account(self, value):
        if not BankAccount.objects.filter(account_number=value).exists():
            raise serializers.ValidationError("Receiver account does not exist")
        return value


class TransactionSerializer(serializers.ModelSerializer):
    sender_account_number = serializers.CharField(source='sender_account.account_number', read_only=True)
    receiver_account_number = serializers.CharField(source='receiver_account.account_number', read_only=True)
    sender_name = serializers.CharField(source='sender_account.user.username', read_only=True)
    receiver_name = serializers.CharField(source='receiver_account.user.username', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_id', 'sender_account_number', 'receiver_account_number',
            'sender_name', 'receiver_name', 'amount', 'description', 'status',
            'flagged', 'fraud_score', 'fraud_reason', 'timestamp'
        ]
        read_only_fields = ['id', 'transaction_id', 'status', 'flagged', 'fraud_score', 'timestamp']
