from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_id', 'sender_account', 'receiver_account',
        'amount', 'status', 'flagged', 'timestamp'
    ]
    list_filter = ['status', 'flagged', 'timestamp']
    search_fields = [
        'transaction_id', 'sender_account__account_number',
        'receiver_account__account_number'
    ]
    readonly_fields = ['transaction_id', 'timestamp', 'updated_at']
