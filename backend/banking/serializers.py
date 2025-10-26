from rest_framework import serializers
from .models import BankAccount


class BankAccountSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = BankAccount
        fields = [
            'id', 'account_number', 'account_type', 'balance',
            'daily_limit', 'is_active', 'user_email', 'user_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'account_number', 'balance', 'created_at', 'updated_at']
