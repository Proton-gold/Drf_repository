from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient
from django.test import TestCase
from accounts.models import User
from accounts.serialazer import LoginSerializer, RegistrationSerializer


class LoginSerializerTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='test')

        data_valid = {
            'username': 'test',
            'password': 'test',
        }

        self.serializer = LoginSerializer(data=data_valid)
        self.client = APIClient()
        self.logout_url ='/accounts/auth/logout/'  # create → list

    def test_registration_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_unauthorized_access(self):
        response = self.client.post(self.logout_url,{'refresh':'test'})
        self.assertEqual(response.status_code, 401)


class RegistrationSerializerTest(TestCase):
    # def setUp(self):
        # self.user = User.objects.create_user(username='username', password='password')

    def test_user_create_password_mismatch(self):
        data_invalid = {
            'username': 'username',
            "password": "password",
            "confirm_password": "password1"
        }
        serializer = RegistrationSerializer(data=data_invalid)
        # serializer.is_valid()
        # serializer.save()

        self.assertFalse(serializer.is_valid())
        # self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
