from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient
from .models import Users
from .serializers import UsersSerializer
import jwt


# This class is to test POST requests
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
