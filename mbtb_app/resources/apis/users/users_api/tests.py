from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Users


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


# This class is to test POST requests for new user accounts
class NewUserRequestTest(APITestCase):

    def setUp(self):
        self.valid_payload = {
            "email": "amamam@gmail.com",
            "title": "Mr.",
            "first_name": "json",
            "middle_name": "",
            "last_name": "json",
            "institution": "dal",
            "department_name": "medical",
            "position_title": "developer",
            "address_line_1": "temp_location",
            "address_line_2": "",
            "city": "city",
            "province": "province",
            "country": "country",
            "postal_code": "postalcode",
            "comments": "this is comment box"
        }

        self.invalid_payload = {
            "email": "",
            "title": "Mr.",
            "first_name": "",
            "middle_name": "",
            "last_name": "",
            "institution": "dal",
            "department_name": "medical",
            "position_title": "developer",
            "address_line_1": "temp_location",
            "address_line_2": "",
            "city": "city",
            "province": "province",
            "country": "country",
            "postal_code": "postalcode",
            "comments": "this is comment box"
        }
        # force authentication for api testing
        self.client.force_authenticate()

    # post request with valid data
    def test_valid_new_request(self):
        response = self.client.post(
            '/add_new_users/',
            self.valid_payload,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    # post request with invalid data
    def test_valid_bad_new_request(self):
        response = self.client.post(
            '/add_new_users/',
            self.invalid_payload,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
