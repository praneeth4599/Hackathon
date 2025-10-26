from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'user_email', 'action', 'ip_address',
            'user_agent', 'details', 'status', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']
