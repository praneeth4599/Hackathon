from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogListView(generics.ListAPIView):
    """
    Endpoint for auditors and admins to view audit logs.
    Regular users cannot access this endpoint.
    """
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow auditors and admins
        if self.request.user.role not in ['admin', 'auditor']:
            return AuditLog.objects.none()

        queryset = AuditLog.objects.all()

        # Optional filtering by user_id
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        # Optional filtering by action
        action = self.request.query_params.get('action')
        if action:
            queryset = queryset.filter(action=action)

        return queryset.order_by('-timestamp')
