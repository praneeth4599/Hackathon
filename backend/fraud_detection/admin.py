from django.contrib import admin
from .models import FraudAlert


@admin.register(FraudAlert)
class FraudAlertAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'transaction', 'severity', 'fraud_score',
        'status', 'reviewed_by', 'created_at'
    ]
    list_filter = ['severity', 'status', 'created_at']
    search_fields = ['transaction__transaction_id', 'detection_reason']
    readonly_fields = ['created_at', 'reviewed_at']
