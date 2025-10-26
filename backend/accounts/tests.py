from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationTestCase(APITestCase):
    """Test suite for user registration"""

    def setUp(self):
        self.register_url = '/api/auth/register/'
        self.valid_payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Test@1234',
            'password2': 'Test@1234',
            'role': 'customer'
        }

    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_user_registration_password_mismatch(self):
        """Test registration fails when passwords don't match"""
        payload = self.valid_payload.copy()
        payload['password2'] = 'DifferentPassword@123'
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_email(self):
        """Test registration fails with duplicate email"""
        self.client.post(self.register_url, self.valid_payload, format='json')
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(APITestCase):
    """Test suite for user login"""

    def setUp(self):
        self.login_url = '/api/auth/login/'
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Test@1234'
        )

    def test_user_login_success(self):
        """Test successful login with valid credentials"""
        payload = {
            'email': 'test@example.com',
            'password': 'Test@1234'
        }
        response = self.client.post(self.login_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        """Test login fails with invalid credentials"""
        payload = {
            'email': 'test@example.com',
            'password': 'WrongPassword'
        }
        response = self.client.post(self.login_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
