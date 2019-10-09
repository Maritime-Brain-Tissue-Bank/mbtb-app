from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import AdminAccount


# This class is to test admin login
class AdminAuthenticationTestCase(APITestCase):

    def setUp(self):
        self.email = 'admin@mbtb.ca'
        self.password = 'asdfghjkl123'
        AdminAccount.objects.create(email=self.email, password_hash=self.password)
        self.valid_credentials = {
            'email': self.email,
            'password': self.password
        }
        self.invalid_credentials = {
            'email': self.email,
            'password': 'asdfghjklp123'
        }
        self.client = APIClient(enforce_csrf_checks=True)  # enforcing csrf checks

    # post request with valid credentials
    def test_valid_admin_login(self):
        response = self.client.post(
            '/admin_auth',
            self.valid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    # post request with invalid credentials
    def test_invalid_admin_login(self):
        response = self.client.post(
            '/admin_auth',
            self.invalid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
