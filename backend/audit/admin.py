from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'action', 'ip_address', 'status', 'timestamp']
    list_filter = ['action', 'status', 'timestamp']
    search_fields = ['user__email', 'ip_address', 'action']
    readonly_fields = ['timestamp']

    def has_add_permission(self, request):
        # Prevent manual creation of audit logs
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of audit logs
        return False
