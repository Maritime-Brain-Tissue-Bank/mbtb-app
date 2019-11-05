from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from register.models import Users


# This class is to test admin login
class UsersAuthenticationTestCase(APITestCase):

    def setUp(self):
        self.email = 'user@mbtb.ca'
        self.password = 'right_password'
        Users.objects.create(email=self.email, password_hash=self.password)
        self.valid_credentials = {
            'email': self.email,
            'password': self.password
        }
        self.invalid_credentials = {
            'email': self.email,
            'password': 'wrong_password'
        }
        self.client = APIClient(enforce_csrf_checks=True)  # enforcing csrf checks

    # post request with valid credentials
    def test_valid_admin_login(self):
        response = self.client.post(
            '/user_auth',
            self.valid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    # post request with invalid credentials
    def test_invalid_admin_login(self):
        response = self.client.post(
            '/user_auth',
            self.invalid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
