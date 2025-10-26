from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import AuditLog

User = get_user_model()


class AuditLogTestCase(TestCase):
    """Test suite for audit logging"""

    def test_audit_log_creation(self):
        """Test that audit logs can be created"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Test@1234',
            role='customer'
        )

        log = AuditLog.objects.create(
            user=user,
            action='login',
            ip_address='127.0.0.1',
            status='success'
        )

        self.assertEqual(log.user, user)
        self.assertEqual(log.action, 'login')
        self.assertEqual(log.status, 'success')


class AuditLogAPITestCase(APITestCase):
    """Test suite for audit log API"""

    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='Test@1234',
            role='admin'
        )

        self.customer_user = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='Test@1234',
            role='customer'
        )

    def test_admin_can_view_logs(self):
        """Test that admin can view audit logs"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/audit/logs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_cannot_view_logs(self):
        """Test that customer cannot view audit logs"""
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get('/api/audit/logs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return empty list for non-admin users
        self.assertEqual(len(response.data['results']), 0)
